import json
import requests
from requests.exceptions import RequestException, Timeout, ConnectionError

# ===== 在这里填入你的 DeepSeek API Key =====
API_KEY = "sk-ab8a5ebeb01645a0a3a4ca618a9b97c9"
# ==========================================

API_URL = "https://api.deepseek.com/chat/completions"
DEFAULT_MODEL = "deepseek-chat"
TIMEOUT_SECONDS = 15


def build_headers(api_key: str) -> dict:
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }


def build_payload(question: str, model: str = DEFAULT_MODEL) -> dict:
    return {
        "model": model,
        "messages": [
            {"role": "user", "content": question}
        ]
    }


def send_question_to_deepseek(question: str) -> dict:
    payload = build_payload(question)
    headers = build_headers(API_KEY)

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=TIMEOUT_SECONDS
        )
    except Timeout:
        raise RuntimeError("请求超时，请检查网络连接或稍后再试。")
    except ConnectionError:
        raise RuntimeError("网络错误，无法连接到 DeepSeek API。请检查网络或代理设置。")
    except RequestException as exc:
        raise RuntimeError(f"请求失败：{exc}")

    try:
        result = response.json()
    except ValueError:
        raise RuntimeError(f"响应不是有效JSON。HTTP状态码：{response.status_code}，响应内容：{response.text}")

    return {
        "status_code": response.status_code,
        "body": result
    }


def extract_answer(api_response: dict) -> str:
    status_code = api_response["status_code"]
    body = api_response["body"]

    if status_code == 401:
        raise RuntimeError("认证失败：请检查 API Key 是否正确。")

    if status_code == 402 or status_code == 403:
        message = body.get("error", {}).get("message") if isinstance(body, dict) else None
        raise RuntimeError(message or "余额不足或权限不足，请检查账户状态。")

    if status_code != 200:
        message = body.get("error", {}).get("message") if isinstance(body, dict) else None
        raise RuntimeError(message or f"API 返回异常状态码：{status_code}")

    if not isinstance(body, dict):
        raise RuntimeError("API 响应格式不正确，无法解析答案。")

    if "error" in body:
        err = body["error"]
        raise RuntimeError(f"API 错误：{err.get('message', '未知错误')}")

    choices = body.get("choices")
    if not choices or not isinstance(choices, list):
        raise RuntimeError("API 响应中缺少 choices 字段。")

    first_choice = choices[0]
    message = first_choice.get("message")
    if not message or not isinstance(message, dict):
        raise RuntimeError("API 响应中缺少 message 字段。")

    content = message.get("content")
    if not content:
        raise RuntimeError("API 响应中缺少回答内容。")

    return content.strip()


def prompt_user() -> str:
    print("\n请输入你的问题（输入 '退出' 或 'exit' 结束）：")
    return input("> ").strip()


def main() -> None:
    if API_KEY.startswith("sk-your-"):
        print("请先在 chatbot.py 中将 API_KEY 替换为你的 DeepSeek API Key。")
        return

    print("DeepSeek 聊天机器人已启动。")

    while True:
        question = prompt_user()
        if not question:
            print("请输入一个问题。")
            continue

        if question.lower() in {"退出", "exit", "quit", "q"}:
            print("已退出。感谢使用！")
            break

        print("正在请求 DeepSeek，请稍候...")
        try:
            api_response = send_question_to_deepseek(question)
            answer = extract_answer(api_response)
            print("\nAI回答：")
            print(answer)
        except RuntimeError as error:
            print(f"\n❌ 出错了：{error}")
            if "余额不足" in str(error) or "权限不足" in str(error):
                print("请检查账户余额或 API Key 权限。")
        except Exception as error:
            print(f"\n❌ 未知错误：{error}")


if __name__ == "__main__":
    main()
