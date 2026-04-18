# Vercel 配置手把手指南

没问题，请跟着这 4 步走，配置完以后你的网页就**自带 AI 能力**了，不用再手动输 Key。

## 第一步：进入 Vercel 项目设置

1. 打开浏览器，登录 [Vercel 控制台](https://vercel.com/dashboard)。
2. 在列表中找到你刚才部署的项目（名字大概是 `trae-article-jike` 或类似的）。
3. 点击项目名称进入详情页。
4. 点击顶部导航栏的 **"Settings"** (设置)。

## 第二步：添加环境变量 (Environment Variables)

1. 在左侧菜单栏点击 **"Environment Variables"**。
2. 你会看到 "Add New" 的输入框。请依次添加下面**两个**变量：

   **变量 1 (OpenAI Key):**
   - **Key**: `OPENAI_API_KEY`
   - **Value**: `<your-openai-api-key>`
   - 点击 **Save** 按钮。

   **变量 2 (Base URL):**
   - **Key**: `OPENAI_BASE_URL`
   - **Value**: `https://api.openai.com/v1`
   - 点击 **Save** 按钮。

   **变量 3 (Model):**
   - **Key**: `OPENAI_MODEL`
   - **Value**: `gpt-5.4`
   - 点击 **Save** 按钮。

## 第三步：重新部署 (让配置生效)

配置好变量后，必须**重新部署一次**才会生效。

1. 点击顶部导航栏的 **"Deployments"** (部署)。
2. 找到列表里最上面的一条（也就是当前的最新版本）。
3. 点击右侧的 **三个点图标 (···)**。
4. 选择 **"Redeploy"**。
5. 在弹出的确认框里直接点 **"Redeploy"** 按钮。

## 第四步：验证

等待 1-2 分钟部署变绿（Ready）后：

1. 打开你的线上网页地址（如 `https://xxxx.vercel.app`）。
2. **不用**点右上角配置 Key。
3. 直接在 "Step 1" 输入框里随便写个测试文本（比如“你好”）。
4. 点击 **"✨ AI 自动生成"**。

如果能成功生成内容，恭喜你，配置成功！🎉
