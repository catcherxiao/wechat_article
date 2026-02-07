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
    vercel env add NEWAPI_API_KEY
    ```
    *   输入你的 Key：`sk-X9EIfcfBO2CdZL4g37AgBZks22JD9K4PUvgDtnYKqy5e5eFU`
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
    *   Key: `NEWAPI_API_KEY`
    *   Value: `sk-X9EIfcfBO2CdZL4g37AgBZks22JD9K4PUvgDtnYKqy5e5eFU`
    *   点击 **"Add"**。

4.  **点击 Deploy**
    等待几秒钟，你的专属 AI 写作工具就上线了！🎉
