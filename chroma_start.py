import chromadb

# 创建本地 Chroma 客户端
client = chromadb.PersistentClient(path="./my_memory_db")

# 创建一个集合，就像创建一个“抽屉”
collection = client.get_or_create_collection(name="my_memories")

# 存入三条关于“我”的记忆
collection.add(
    documents=[
        "我喜欢打篮球，每周都会去球场练习投篮。",
        "我毕业于计算机科学专业，擅长 Python 编程。",
        "我养了一只叫小橘的橘猫，它很爱吃零食。"
    ],
    ids=["1", "2", "3"]
)

print("已存入三条个人记忆。")

# 查询：找到与我运动爱好相关的记忆
query = "我喜欢什么运动？"
results = collection.query(
    query_texts=[query],
    n_results=1
)

print(f"\n查询: {query}")
print(f"最相关的记忆: {results['documents'][0][0]}")
print(f"距离分数: {results['distances'][0][0]:.4f}")
