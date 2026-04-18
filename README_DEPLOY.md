# 🚀 如何发布到 Vercel

你的项目已经准备就绪，可以随时部署到 Vercel。由于当前环境限制，请按照以下步骤在你的本地终端或 Vercel 网页端操作。

## 方法一：使用 Vercel CLI（推荐）

如果你熟悉命令行，这是最快的方法。

1.  **安装 Vercel CLI** (如果尚未安装)
    ```bash
    npm install -g vercel
    ```

2.  **登录 Vercel**
    ```bash
    vercel login
    ```

3.  **部署项目**
    在项目根目录下运行：
    ```bash
    vercel --prod
    ```
    *   一路回车确认即可。

4.  **配置环境变量 (重要！)**
    部署完成后，AI 功能可能暂时无法使用 (401 错误)，因为云端还没有配置 API Key。
    *   运行以下命令配置环境变量（或者去 Vercel 网页控制台设置）：
    ```bash
    vercel env add OPENAI_API_KEY
    ```
    *   输入你的 Key：`<your-openai-api-key>`
    *   可选配置模型：
    ```bash
    vercel env add OPENAI_MODEL
    ```
    *   Value：`gpt-5.4`
    *   选择环境：全选 (Production, Preview, Development)
    *   **重新部署**以生效：
    ```bash
    vercel --prod
    ```

---

## 方法二：使用 GitHub + Vercel 网页端

如果你更喜欢图形化界面：

1.  **推送到 GitHub**
    ```bash
    git remote add origin <你的仓库地址>
    git push -u origin master
    ```

2.  **在 Vercel 导入项目**
    *   打开 [Vercel Dashboard](https://vercel.com/dashboard)
    *   点击 **"Add New..."** -> **"Project"**
    *   选择刚才推送的 GitHub 仓库并导入。

3.  **设置环境变量**
    *   在导入页面的 **"Environment Variables"** 区域：
    *   Key: `OPENAI_API_KEY`
    *   Value: `<your-openai-api-key>`
    *   Key: `OPENAI_MODEL`
    *   Value: `gpt-5.4`
    *   点击 **"Add"**。

4.  **点击 Deploy**
    等待几秒钟，你的专属 AI 写作工具就上线了！🎉

---

## 方法三：服务器 systemd 部署

这个项目不需要前端构建链。服务器部署时直接运行 `local_server.js`，它会同时提供静态页面、`prompts/*.md` 和 `/api/proxy`。

推荐环境变量：

```bash
PORT=3001
HOST=0.0.0.0
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-5.4
OPENAI_REASONING_EFFORT=none
OPENAI_API_KEY=<your-openai-api-key>
ARTICLE_JIKE_ACCESS_TOKEN=<your-login-token>
```

`ARTICLE_JIKE_ACCESS_TOKEN` 是访问本站的登录密钥。配置后，浏览器只需要在“设置”里填写这个访问密钥，不需要填写 OpenAI API Key；AI 请求由服务器用 `OPENAI_API_KEY` 转发。

最小 systemd 服务：

```ini
[Unit]
Description=Article Jike WeChat Workflow
Wants=network-online.target
After=network-online.target

[Service]
Type=simple
User=ubuntu
Group=ubuntu
WorkingDirectory=/opt/article-jike
EnvironmentFile=/etc/article-jike.env
ExecStart=/usr/bin/node /opt/article-jike/local_server.js
Restart=on-failure
RestartSec=3

[Install]
WantedBy=multi-user.target
```

上线检查：

```bash
node --check /opt/article-jike/local_server.js
sudo systemctl daemon-reload
sudo systemctl enable --now article-jike.service
systemctl is-active article-jike.service
curl -I http://127.0.0.1:3001/wechat_workflow.html
curl http://127.0.0.1:3001/api/status
```

如果需要公网直接访问，服务器防火墙和云厂商安全组都要放行对应端口。不要为了绕过安全组直接复用已有 `80/443` 入口，除非已经确认不会影响现有服务。
