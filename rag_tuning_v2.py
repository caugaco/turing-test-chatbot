# rag_tuning_v2.py —— 防呆版，保证有输出
import sys
import traceback

# 强制实时输出（即使 -u 无效也能工作）
try:
    sys.stdout.reconfigure(line_buffering=True)
    sys.stderr.reconfigure(line_buffering=True)
except:
    pass

print("脚本开始执行...", flush=True)

try:
    import re
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    from langchain_openai import ChatOpenAI
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    print("所有模块导入成功", flush=True)
except Exception as e:
    print(f"导入模块失败：{e}", flush=True)
    traceback.print_exc()
    sys.exit(1)

# 读取 Key
try:
    with open("key.txt", "r") as f:
        raw_key = f.read().strip()
    cleaned_key = re.sub(r'[^!-~]', '', raw_key)
    print(f"Key 已加载，前8位：{cleaned_key[:8]}...", flush=True)
except Exception as e:
    print(f"Key 读取失败：{e}", flush=True)
    sys.exit(1)

# 读取文档
try:
    with open("knowledge.txt", "r", encoding="utf-8") as f:
        full_text = f.read()
    print(f"文档已读取，长度：{len(full_text)} 字符", flush=True)
except Exception as e:
    print(f"knowledge.txt 读取失败，请确认文件已创建：{e}", flush=True)
    sys.exit(1)

# 参数配置
configs = [
    {"chunk_size": 200, "overlap": 30},
    {"chunk_size": 500, "overlap": 50},
    {"chunk_size": 1000, "overlap": 100},
]
question = "RAG 有什么优点？"

# 初始化大模型
try:
    llm = ChatOpenAI(
        model="deepseek-chat",
        openai_api_key=cleaned_key,
        openai_api_base="https://api.deepseek.com/v1",
        temperature=0.3,
    )
    print("大模型初始化成功", flush=True)
except Exception as e:
    print(f"大模型初始化失败：{e}", flush=True)
    sys.exit(1)

# 开始实验
print("\n=== 切片参数对比实验 ===\n", flush=True)
for cfg in configs:
    try:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=cfg["chunk_size"],
            chunk_overlap=cfg["overlap"],
            separators=["\n\n", "\n", "。", "！", "？", "；", "，", " ", ""]
        )
        chunks = splitter.split_text(full_text)

        vectorizer = TfidfVectorizer()
        chunk_vectors = vectorizer.fit_transform(chunks)
        query_vec = vectorizer.transform([question])
        scores = cosine_similarity(query_vec, chunk_vectors).flatten()
        top_idx = scores.argsort()[-2:][::-1]
        retrieved = [chunks[i] for i in top_idx]
        context = "\n".join(retrieved)

        messages = [
            ("system", "基于资料回答，不要编造。"),
            ("human", f"资料：\n{context}\n\n问题：{question}")
        ]
        answer = llm.invoke(messages).content

        print(f"【chunk_size={cfg['chunk_size']}, overlap={cfg['overlap']}】", flush=True)
        print(f"切块数：{len(chunks)}", flush=True)
        for i, r in enumerate(retrieved, 1):
            print(f"  片段{i}：{r[:80]}...", flush=True)
        print(f"AI回答前200字：{answer[:200]}...", flush=True)
        print("-" * 60, flush=True)
    except Exception as e:
        print(f"实验出错（{cfg}）：{e}", flush=True)
        traceback.print_exc()

print("脚本执行完毕。", flush=True)