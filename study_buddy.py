# study_buddy.py —— AI 学伴网页版
try:
    import re
    import socket
    from pathlib import Path
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    from langchain_openai.chat_models import ChatOpenAI
    from langchain_core.messages import HumanMessage, SystemMessage
    import gradio as gr
except ModuleNotFoundError as exc:
    missing = exc.name
    raise SystemExit(
        f"缺少依赖模块：{missing}\n"
        "请先激活工作区虚拟环境并安装依赖：\n"
        "  .venv\\Scripts\\activate\n"
        "  python -m pip install -r requirements.txt\n"
        "然后执行：\n"
        "  python study_buddy.py\n"
        "如果你不想激活虚拟环境，也可以直接运行：\n"
        "  .venv\\Scripts\\python.exe study_buddy.py\n"
    ) from exc

BASE_DIR = Path(__file__).resolve().parent
KEY_FILE = BASE_DIR / "key.txt"
NOTES_FILE = BASE_DIR / "my_notes.txt"

if not KEY_FILE.exists():
    raise SystemExit("未找到 key.txt，请把 Key 放在 study_buddy.py 同目录下。")
if not NOTES_FILE.exists():
    raise SystemExit("未找到 my_notes.txt，请把学习笔记放在 study_buddy.py 同目录下。")

# ── 加载 Key ──
with KEY_FILE.open("r", encoding="utf-8") as f:
    key = re.sub(r"[^!-~]", "", f.read().strip())

# ── 加载知识库 ──
text = NOTES_FILE.read_text(encoding="utf-8").strip()
if not text:
    raise SystemExit("my_notes.txt 为空，请填写学习资料后重试。")

# ── 切片 + 索引 ──

def split_text(text, chunk_size=500):
    if not text:
        return []

    sentences = re.split(r"(?<=[。！？\n])", text)
    chunks = []
    current = ""

    for sentence in sentences:
        candidate = current + sentence
        if len(candidate) <= chunk_size:
            current = candidate
        else:
            if current:
                chunks.append(current.strip())
            if len(sentence) <= chunk_size:
                current = sentence
            else:
                for i in range(0, len(sentence), chunk_size):
                    chunks.append(sentence[i : i + chunk_size].strip())
                current = ""

    if current:
        chunks.append(current.strip())

    return [chunk for chunk in chunks if chunk]

chunks = split_text(text, chunk_size=500)
if not chunks:
    raise SystemExit("文本拆分结果为空，请检查 my_notes.txt 内容是否正确。")
vectorizer = TfidfVectorizer()
chunk_vectors = vectorizer.fit_transform(chunks)

# ── 大模型 ──
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=key,
    base_url="https://api.deepseek.com/v1",
    temperature=0.5,
)

# ── RAG 问答 ──
def ask_question(message, history):
    if not message.strip():
        return "请输⼊问题～"
    # 检索 top 2 片段
    qv = vectorizer.transform([message])
    scores = cosine_similarity(qv, chunk_vectors).flatten()
    top_idx = scores.argsort()[-2:][::-1]
    context = "\n".join([chunks[i] for i in top_idx])

    msgs = [
        SystemMessage(content="你是AI学伴小伴，请基于资料温柔回答，资料没有就说不知道。"),
        HumanMessage(content=f"资料：\n{context}\n\n问题：{message}"),
    ]
    return llm.invoke(msgs).content

# ── Gradio 界面 ──
demo = gr.ChatInterface(
    fn=ask_question,
    title="🎓 AI 学伴 · 小伴",
    description="上传你的学习笔记，我就是你的专属复习伙伴～",
)

def find_free_port(start_port=7860, max_port=7900):
    for port in range(start_port, max_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    raise RuntimeError(f"无法在端口范围 {start_port}-{max_port} 内找到可用端口")

if __name__ == "__main__":
    port = find_free_port(7860, 7900)
    print(f"启动 Gradio，访问地址 http://127.0.0.1:{port}")
    demo.launch(server_name="127.0.0.1", server_port=port)