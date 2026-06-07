from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

sentence1 = "今天天气真好"
sentence2 = "今日气候宜人"

# 使用字符级 n-gram（1到3个连续字符），无需分词器
vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(1, 3))
tfidf_matrix = vectorizer.fit_transform([sentence1, sentence2])
similarity = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]

print(f"句子1: {sentence1}")
print(f"句子2: {sentence2}")
print(f"相似度: {similarity:.4f}")
