import os
import requests
import json

# 从环境变量获取Cookie
COOKIE = os.environ.get('GLADOS_COOKIE')

def check_in():
    url = "https://glados.space/api/user/checkin"
    origin = "https://glados.space"
    referer = "https://glados.space/console/checkin"
    
    payload = {
        'token': "glados.network"
    }
    
    headers = {
        'cookie': COOKIE,
        'origin': origin,
        'referer': referer,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'content-type': 'application/json'
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        result = response.json()
        
        if result['code'] == 0:
            message = result['message']
            days = result['list'][0]['balance']
            return f"{message} - 剩余天数: {days}"
        return f"签到失败: {result.get('message', '未知错误')}"
    except Exception as e:
        return f"请求异常: {str(e)}"

if __name__ == '__main__':
    print(check_in())
    