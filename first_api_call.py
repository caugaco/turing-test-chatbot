import requests

url = "https://api.deepseek.com/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer sk-8426cdf3f30f47bc9507f818b6ba859f"
}
data = {
    "model": "deepseek-chat",
    "messages": [
        {"role": "user", "content": "用一句话解释什么是图灵测试"}
    ]
}

response = requests.post(url, headers=headers, json=data)
result = response.json()

answer = result["choices"][0]["message"]["content"]
print("AI说:", answer)