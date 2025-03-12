# GLaDosCheckin163
 
## 一、 配置步骤：
   1. 登录GLaDOS网站，通过浏览器开发者工具获取Cookie
   2. 在GitHub仓库的 Settings > Secrets 中添加名为 `GLADOS_COOKIE` 的加密secret
   3. 将两个文件提交到仓库

## 二、注意事项：
1. Cookie有效期通常为1个月，到期后需要更新
2. 北京时间22:00对应UTC时间14:00
3. 建议先手动触发工作流测试功能
4. 不要公开分享你的Cookie信息
5. 如果网站接口变更需要同步更新脚本

## 三、验证：可以通过以下方式验证结果：
1. 在GitHub Actions的运行日志中查看输出
2. 登录GLaDOS网站确认签到状态
3. 检查是否收到签到成功的邮件通知（如果网站有此功能）
为了实现GLaDOS的自动签到，请按以下步骤操作：

## 四、原始代码
1. 创建Python脚本 (`checkin.py`)：

```python
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
```

2. 创建GitHub Action工作流 (`.github/workflows/checkin.yml`)：

```yaml
name: GLaDOS Auto Checkin

on:
  schedule:
    - cron: '0 14 * * *'  # UTC时间14:00（北京时间22:00）
  workflow_dispatch:  # 允许手动触发

jobs:
  checkin:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.x'

      - name: Install dependencies
        run: pip install requests

      - name: Run checkin
        env:
          GLADOS_COOKIE: ${{ secrets.GLADOS_COOKIE }}
        run: |
          result=$(python checkin.py)
          echo "result=$result" >> $GITHUB_OUTPUT

      - name: Show result
        run: echo "${{ steps.checkin.outputs.result }}"
```

##（🌹 End 🌹）