import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

# =================================================
# 请把下面引号内的内容替换成你的真实API Key，保留英文引号
os.environ["OPENAI_API_KEY"] = "你的DeepSeek_API_Key"
# =================================================

memories = [
    "我喜欢打篮球，每周都会去球场练习投篮。",
    "我毕业于计算机科学专业，擅长 Python 编程。",
    "我养了一只叫小橘的橘猫，它很爱吃零食。"
]

def retrieve(query):
    """用 TF-IDF 找出最相似的记忆"""
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform([query] + memories)
    similarities = cosine_similarity(tfidf[0:1], tfidf[1:])[0]
    best_idx = similarities.argmax()
    return memories[best_idx]

llm = ChatOpenAI(
    model="deepseek-chat",
    base_url="https://api.deepseek.com/v1",
    api_key=os.environ["OPENAI_API_KEY"],
    temperature=0.3
)

questions = [
    "我喜欢什么运动？",
    "根据我的爱好，推荐一个周末活动",
    "我养了什么宠物？"
]

for q in questions:
    best = retrieve(q)
    prompt = f"请仅基于以下记忆内容回答问题。记忆：“{best}”\n问题：{q}"
    answer = llm([HumanMessage(content=prompt)])
    print(f"🧑 用户: {q}")
    print(f"🔍 匹配记忆: {best}")
    print(f"🤖 AI: {answer.content}\n")
