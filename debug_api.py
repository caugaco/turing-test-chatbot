import requests
import json

# ====== 注意：此Key已公开，请务必重置 ======
API_KEY = "sk-8426cdf3f30f47bc9507f818b6ba859f"
# ==========================================

url = "https://api.deepseek.com/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}
data = {
    "model": "deepseek-chat",
    "messages": [
        {"role": "user", "content": "用一句话解释什么是图灵测试"}
    ]
}

print("正在请求...")
response = requests.post(url, headers=headers, json=data)

print(f"状态码: {response.status_code}")

try:
    resp_json = response.json()
    print("完整响应:")
    print(json.dumps(resp_json, indent=2, ensure_ascii=False))
except Exception:
    print("响应不是标准JSON，原始文本:")
    print(response.text)