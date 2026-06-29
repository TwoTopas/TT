# DeepSeek本地代理模式（微信小程序开发）

## 适用场景
微信小程序需要调用DeepSeek API，但：
1. 小程序白名单域名限制（wx.request不能调外部API）
2. 不想暴露API Key在客户端代码中
3. 需要本地调试、快速迭代

## 架构

```
小程序 → http://127.0.0.1:PORT/api/report → Python代理 → DeepSeek API
```

## 实现方案

### Python代理服务器

```python
import http.server, json, os
from urllib import request

class ProxyHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers['Content-Length'])).decode('utf-8', errors='replace'))
        module = body.get('module', 'assess')
        # ... build prompt from module
        result = call_deepseek(prompt)
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({'report': result}, ensure_ascii=False).encode())
```

### 小程序端调用

```javascript
wx.request({
  url: 'http://127.0.0.1:PORT/api/report',
  method: 'POST',
  data: { module: 'assess', category: '...', ... },
  success(res) { /* use res.data.report */ },
  fail() { /* fallback to static data */ }
})
```

## 开发者工具配置

必须勾选：详情 → 本地设置 → 「不校验合法域名」

## 端口冲突解决

多个代理实例会导致端口被占用：
```bash
netstat -ano | grep PORT | grep LISTENING
# 改端口号: port = 8789
```
