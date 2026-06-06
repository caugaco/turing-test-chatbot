import requests
import json

# ===== 在这里填入你的 DeepSeek API Key =====
API_KEY = "sk-ab8a5ebeb01645a0a3a4ca618a9b97c9"
# ===========================================

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
status = response.status_code
print(f"状态码: {status}")

try:
    resp = response.json()
except Exception:
    print("❌ 响应不是JSON格式，原始返回:")
    print(response.text)
    exit()

# 打印完整响应以便排查
print("完整响应:")
print(json.dumps(resp, indent=2, ensure_ascii=False))

# 尝试提取回答
if status == 200 and "choices" in resp:
    answer = resp["choices"][0]["message"]["content"]
    print("\n✅ 成功！AI说:", answer)
elif "error" in resp:
    err = resp["error"]
    print(f"\n❌ API返回错误: {err.get('message', '未知错误')}")
    if "Insufficient Balance" in err.get("message", ""):
        print("💡 余额不足，请切换至阿里云百炼方案（见下方）。")
elif status == 401:
    print("💡 认证失败，请检查API Key是否正确。")
else:
    print("💡 遇到未知情况，请把上面打印的完整响应发给我。")