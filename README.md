# GLaDosCheckin163
 
## 一、 配置步骤：
   1. 登录GLaDOS网站，通过浏览器开发者工具获取Cookie
   2. 在GitHub仓库的 Settings > Secrets 中添加名为 `GLADOS_COOKIE` 的加密secret
   3. 将两个文件提交到仓库

## 二、​获取 GLaDOS 的 Cookie
	1. 登录 GLaDOS 并打开签到页面：https://glados.space/console/checkin。
	2. 按下 F12 打开浏览器开发者工具，切换到 ​Network（网络）​ 标签页。
	3. 点击页面上的 ​Checkin（签到）​ 按钮，找到名为 checkin 或 status 的请求，在 ​Headers 中复制完整的 Cookie 值（格式类似 koa:sess=xxxx; koa:sess.sig=xxxx）。

## 三、注意事项：
1. Cookie有效期通常为1个月，到期后需要更新
2. 北京时间22:00对应UTC时间14:00
3. 建议先手动触发工作流测试功能
4. 不要公开分享你的Cookie信息
5. 如果网站接口变更需要同步更新脚本

## 四、验证：可以通过以下方式验证结果：
1. 在GitHub Actions的运行日志中查看输出
2. 登录GLaDOS网站确认签到状态
3. 检查是否收到签到成功的邮件通知（如果网站有此功能）
为了实现GLaDOS的自动签到，请按以下步骤操作：

## 五、原始代码
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

##（🌹🌹🌹🌹🌹🌹🌹🌹🌹🌹补充：）


# GLaDOS 自动签到的两种方法：

以下是针对 **GLaDOS 自动签到**的代码生成与实现方案，结合搜索结果的两种主流方法（GitHub Actions 和青龙面板脚本）进行说明：

### 方法一：通过 **Python 脚本 + GitHub Actions** 实现自动签到
#### 1. **获取 GLaDOS 的 Cookie**
   • 登录 GLaDOS 并打开签到页面：`https://glados.space/console/checkin`。
   • 按下 `F12` 打开浏览器开发者工具，切换到 **Network（网络）** 标签页。
   • 点击页面上的 **Checkin（签到）** 按钮，找到名为 `checkin` 或 `status` 的请求，在 **Headers** 中复制完整的 `Cookie` 值（格式类似 `koa:sess=xxxx; koa:sess.sig=xxxx`）。

#### 2. **编写 Python 脚本**
```python
import requests

# 签到 API
url = "https://glados.space/api/user/checkin"
headers = {
    "Content-Type": "application/json",
    "Cookie": "YOUR_COOKIE",  # 替换为实际 Cookie
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
data = {"token": "glados.network"}

response = requests.post(url, headers=headers, json=data)
result = response.json()

if response.status_code == 200:
    message = f"签到成功！剩余天数：{result.get('days')} 天"
else:
    message = f"签到失败：{result.get('message')}"
print(message)
```

#### 3. **部署到 GitHub Actions**
   • **Fork 仓库**：访问 [xianzhichen/checkin](https://github.com/xianzhichen/checkin)，点击右上角 `Fork`。
   • **添加 Cookie**：在仓库的 `Settings → Secrets → Actions` 中新建 Secret：
     ◦ **Name**: `GLADOS`
     ◦ **Value**: 复制的 Cookie 值。
   • **启用定时任务**：GitHub Actions 已预设每天 00:10（UTC+8）自动执行，无需修改代码。

---

### 方法二：通过 **青龙面板** 实现自动签到
#### 1. **安装青龙面板**
   • 参考青龙面板官方文档部署环境（支持 Docker、Linux 等）。

#### 2. **添加 GLaDOS 签到脚本**
   • 在青龙面板的 **脚本管理** 中，添加仓库：
     ◦ **名称**：`GLaDOS_Checkin`
     ◦ **类型**：`公开仓库`
     ◦ **链接**：`https://github.com/hennessey-v/GlaDOS_Checkin_ql.git`
   • 拉取脚本后，在 **环境变量** 中添加 `GLADOS_COOKIE`（值为 Cookie）。

#### 3. **设置定时任务**
   • 在青龙面板的 **定时任务** 中新建任务：
     ◦ **名称**：`GLaDOS 自动签到`
     ◦ **命令**：`task GlaDOS_Checkin_ql/checkin.py`
     ◦ **定时规则**：`0 0 * * *`（每天 0 点执行）。

---

### 补充说明
1. **通知推送**（可选）：
   • 使用 **PushPlus** 微信通知：在 GitHub Actions 或青龙面板中添加 `NOTIFY` Secret，填入 PushPlus 的 Token。
2. **安全性**：
   • **Cookie 需保密**，避免泄露到公开仓库。
3. **合规性**：
   • 确保符合 GLaDOS 服务条款，避免频繁请求导致封号。

---

以上两种方法均可稳定实现自动签到。推荐 **GitHub Actions** 方案（无需服务器），适合新手；**青龙面板** 适合已有相关环境的用户。如需完整代码或配置细节，可参考对应仓库文档。