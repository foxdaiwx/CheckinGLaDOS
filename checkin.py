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
        'token': "glados.one"
    }
    
    headers = {
        'cookie': COOKIE,
        'origin': origin,
        'referer': referer,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        'content-type': 'application/json; charset=utf-8'
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        result = response.json()
        
        #Code=0,表示代码运行成功，然后获取关联信息并显示
        if result['code'] == 0:     #结果可以在页面F12，按checkin，在tab的network-preview 和 response中查看 
            #获取代码运行结果的信息
            message = result['message']
            #获取积分总点数
            points = result['list'][0]['balance']
            #回复前面获取的信息和各个值
            return f"{message} - 总积分: {points}"
        #否则，code<>0，则显示出错信息，比如Invalid Token，可能是Cookie过期或不对
        return f"签到失败: {result.get('message', '未知错误')}"
    #其他情况，比如代码出错、网络问题等，比如connection error；
    except Exception as e:
        return f"请求异常: {str(e)}"

if __name__ == '__main__':
    result = check_in()
    print(result)
    # 将结果写入文本文件
    with open("checkin_result.txt", "w", encoding="utf-8") as file:
        file.write(result)
