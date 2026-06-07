from sentence_transformers import SentenceTransformer, util


CANDIDATE_WORDS = [
    "苹果", "香蕉", "橘子", "天气", "雨天", "晴天", "春天", "夏天", "秋天", "冬天",
    "快乐", "悲伤", "兴奋", "安静", "空气", "风景", "城市", "乡村", "山川", "海洋",
    "学习", "工作", "游戏", "电影", "音乐", "书籍", "美食", "旅行", "健康", "幸福",
    "狗", "猫", "鸟", "鱼", "自然", "文化", "历史", "科技", "未来", "梦想",
    "爱情", "友谊", "家庭", "学校", "老师", "学生", "医生", "教师", "运动", "比赛"
]


def load_model():
    return SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")


def compute_embeddings(model, words):
    return model.encode(words, convert_to_tensor=True)


def select_initial_guess(words, embeddings):
    similarities = util.cos_sim(embeddings, embeddings).mean(dim=1)
    best_index = int(similarities.argmax())
    return words[best_index], embeddings[best_index]


def choose_next_guess(candidates, candidate_embeddings, guessed_indices):
    remaining_indices = [i for i in range(len(candidates)) if i not in guessed_indices]
    if not remaining_indices:
        return None, None, None
    remaining_embeddings = candidate_embeddings[remaining_indices]
    centroid = remaining_embeddings.mean(dim=0)
    scores = util.cos_sim(remaining_embeddings, centroid).squeeze(1)
    best_rel = int(scores.argmax())
    best_index = remaining_indices[best_rel]
    return candidates[best_index], candidate_embeddings[best_index], best_index


def filter_candidates(candidates, candidate_embeddings, guess_embedding, feedback_similarity, tolerance):
    similarities = util.cos_sim(candidate_embeddings, guess_embedding).squeeze(1).tolist()
    filtered = [
        (word, emb)
        for word, emb, sim in zip(candidates, candidate_embeddings, similarities)
        if abs(sim - feedback_similarity) <= tolerance
    ]
    if filtered:
        filtered_words, filtered_embeddings = zip(*filtered)
        return list(filtered_words), util.stack(list(filtered_embeddings))
    return [], None


def main():
    print("词语猜测游戏")
    print("你提前想好一个词语，我会根据你给出的相似度反馈猜词。")
    print("如果你想用自己的词语库，请先修改脚本中的 CANDIDATE_WORDS 列表。\n")

    model = load_model()
    candidates = CANDIDATE_WORDS.copy()
    embeddings = compute_embeddings(model, candidates)
    guessed_indices = []
    round_count = 0

    guess, guess_embedding = select_initial_guess(candidates, embeddings)
    guess_index = candidates.index(guess)

    while True:
        round_count += 1
        print(f"第 {round_count} 轮猜测：{guess}")
        feedback = input("请输入你预设词语与我这个猜测的余弦相似度（0~1），或输入 q 结束：").strip()
        if feedback.lower() == "q":
            print("游戏结束。谢谢参与！")
            break

        try:
            similarity = float(feedback)
        except ValueError:
            print("请输入合法的浮点数相似度，如 0.75。")
            continue

        guessed_indices.append(guess_index)
        tolerance = max(0.05, 0.2 - 0.02 * min(round_count, 5))

        remaining_words, remaining_embeddings = filter_candidates(
            candidates, embeddings, guess_embedding, similarity, tolerance
        )

        if not remaining_words:
            print("当前候选词已被排除，可能需要放宽相似度容差或扩大候选词列表。")
            break

        if len(remaining_words) == 1:
            print(f"我猜到了！你预设的词语很可能是：{remaining_words[0]}")
            break

        candidates = remaining_words
        embeddings = remaining_embeddings

        guess, guess_embedding, guess_index = choose_next_guess(candidates, embeddings, guessed_indices)
        if guess is None:
            print("没有可继续猜测的词语了。")
            break

    print("游戏结束。")


if __name__ == "__main__":
    main()
