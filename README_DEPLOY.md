# 公众号工作流网页版 - 部署指南

由于本工具是纯静态 HTML 页面（AI 调用逻辑在浏览器端运行），因此**不需要复杂的后端服务器**。

推荐使用以下两种“轻运维”部署方式：

## 方式一：Vercel / GitHub Pages (推荐，最简单)

这是最省心的方式，完全免费，无需管理服务器。

1.  **准备代码**
    确保你的代码库包含：
    - `wechat_workflow.html`
    - `prompts/` 文件夹

2.  **部署到 Vercel**
    - 注册/登录 [Vercel](https://vercel.com)。
    - 点击 "Add New Project" -> 导入你的 GitHub 仓库。
    - 在 Build Output Settings 中，将 **Output Directory** 设置为 `.` (当前目录)。
    - 部署成功后，访问 `https://your-project.vercel.app/wechat_workflow.html` 即可。

3.  **关于 API Key**
    - 方案 1（推荐）：在 Vercel 项目里配置环境变量，让网页无需手动输入 Key。
      - `NEWAPI_API_KEY`: `sk-X9EIfcfBO2CdZL4g37AgBZks22JD9K4PUvgDtnYKqy5e5eFU`
      - `NEWAPI_BASE_URL`: `https://api.newapi.pro/v1`
    - 方案 2：部署后打开网页，点击右上角的 **“内容本地处理 (点此配置 AI)”**，把 Key 存到你自己浏览器的 `localStorage`。

## 本地开发配置 (.env.local)

为了方便本地开发时不重复输入 Key，你可以在项目根目录创建 `.env.local` 文件（**不要提交到 GitHub**）：

```bash
NEWAPI_API_KEY=sk-X9EIfcfBO2CdZL4g37AgBZks22JD9K4PUvgDtnYKqy5e5eFU
NEWAPI_BASE_URL=https://api.newapi.pro/v1
```

本地 Vercel 环境会自动读取该文件。

---

## 方式二：Docker 部署 (如果你有云服务器)

如果你更习惯使用 Docker，可以使用我们提供的 `Dockerfile`。

1.  **构建镜像**
    在项目根目录下运行：
    ```bash
    docker build -t wechat-workflow .
    ```

2.  **运行容器**
    ```bash
    docker run -d -p 8080:80 --name my-workflow wechat-workflow
    ```

3.  **访问**
    打开浏览器访问 `http://你的服务器IP:8080`。

---

## 配置 AI 服务

网页内置了对 OpenAI 兼容接口的支持（如 New API）。

1. 点击网页右上角的蓝色小圆点。
2. 填入配置信息：
   - **API Base URL**: `https://api.newapi.pro/v1` (或其他中转地址)
   - **API Key**: `sk-...` (请妥善保管，建议只保存在自己浏览器里)
   - **Model Name**: `gemini-1.5-pro-latest` (或 `gpt-4o`, `claude-3-5-sonnet` 等)
3. 点击保存。

现在，你可以在 Step 1 和 Step 2 中点击 **“✨ AI 自动生成”** 按钮，直接让 AI 帮你写稿和排版了！
