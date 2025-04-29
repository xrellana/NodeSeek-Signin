# -- coding: utf-8 --
import os
from curl_cffi import requests

# NS_RANDOM = os.environ.get("NS_RANDOM", "true") # Keep os import if needed later

def sign(cookie):
    """
    Performs the NodeSeek sign-in action using the provided cookie.

    Args:
        cookie (str): The NodeSeek session cookie.

    Returns:
        tuple: A tuple containing the status string and the message from the API.
               Possible statuses: "success", "already_signed", "invalid_cookie",
                                 "fail", "error", "no_cookie".
    """
    if not cookie:
        print("请先设置Cookie")
        return "no_cookie", ""

    # url = f"https://www.nodeseek.com/api/attendance?random={NS_RANDOM}" # Original URL using NS_RANDOM
    url = f"https://www.nodeseek.com/api/attendance?random=false" # URL as seen in the last read
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
        'origin': "https://www.nodeseek.com",
        'referer': "https://www.nodeseek.com/board",
        'Cookie': cookie
    }

    try:
        # Using curl_cffi requests
        response = requests.post(url, headers=headers, impersonate="chrome110")
        response_data = response.json()
        print(f"签到返回: {response_data}")
        message = response_data.get('message', '')

        # Simplified logic based on observed patterns
        if "鸡腿" in message or response_data.get('success') == True:
            print(f"签到成功: {message}")
            return "success", message
        elif "已完成签到" in message:
            print(f"已经签到过: {message}")
            return "already_signed", message
        elif message == "USER NOT FOUND" or response_data.get('status') == 404:
            print("Cookie已失效")
            return "invalid_cookie", message
        else:
            print(f"签到失败: {message}")
            return "fail", message

    except Exception as e:
        print("发生异常:", e)
        # Attempt to provide more details from the exception if possible
        error_details = str(e)
        if hasattr(e, 'response') and hasattr(e.response, 'text'):
             error_details += f"\nResponse Text: {e.response.text}"
        return "error", error_details

if __name__ == "__main__":
    # Get cookie from user input for testing
    test_cookie = input("请输入您的 NodeSeek Cookie 进行测试: ")
    if test_cookie:
        print("\n--- 开始测试签到 ---")
        status, msg = sign(test_cookie)
        print(f"\n--- 测试结果 ---")
        print(f"状态: {status}")
        print(f"消息: {msg}")
        print("------------------")
    else:
        print("未输入Cookie，测试取消。")
