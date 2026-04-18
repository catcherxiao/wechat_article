<div align="center">

# 投资智慧回响

> *「投资很简单，但并不容易。」* —— 巴菲特

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Vercel](https://img.shields.io/badge/Deploy-Vercel-black)](./VERCEL_GUIDE.md)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED)](./Dockerfile)
<br>

**把巴菲特、芒格、段永平的投资智慧，做成一个能交互、能生成 Prompt、能润色文章的写作工具。**
<br>

不是复读金句。  
是把「买股票就是买公司 / 能力圈 / 护城河 / 长期主义」真正做成一个可用的内容创作系统。

[效果示例](#效果示例) · [快速开始](#快速开始) · [核心功能](#核心功能) · [项目结构](#项目结构) · [部署方式](#部署方式)

</div>

---

## 效果示例

```text
用户  ❯ 帮我润色一篇关于泡泡玛特投资分析的文章

系统  ❯ 正在检索大师语录...
      ✓ 匹配到 5 条相关语录
      ✓ 巴菲特："价格是你付出的，价值是你得到的。"
      ✓ 段永平："关注生意本身，而不是股价。"
      ✓ 王宁："我们远比自己想象的要更感性。"

      正在构建风格化 Prompt...

      ========================================
      # Role
      你是一位拥有20年经验的顶级价值投资者...
      
      # Task
      请将用户输入的文章重写为一篇具有深度洞察力的投资笔记
      ========================================
```

```text
用户  ❯ 输入草稿：收藏玩具变成悦己消费...

系统  ❯ 生成结构化 Prompt，包含：
      - 角色设定（价值投资者视角）
      - 思维模型（护城河分析、生意分类）
      - 相关语录引用（自动匹配）
      - 输出格式要求（Markdown、小标题、层层递进）
```

---

## 快速开始

### 1. 配置 API Key（重要）

本项目需要配置 AI 平台的 API Key 才能正常使用。复制环境变量模板并填写你的密钥：

```bash
cp .env.example .env
```

编辑 `.env` 文件，配置以下任一种方式：

**方式一：OpenAI 官方**
```bash
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-5.4
OPENAI_API_KEY=sk-your-openai-api-key
```

**方式二：兼容 OpenAI 格式的国内平台**
```bash
# 通义千问
OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
OPENAI_MODEL=qwen-max
OPENAI_API_KEY=sk-your-qwen-api-key

# 或 MiniMax
OPENAI_BASE_URL=https://api.minimax.chat/v1
OPENAI_MODEL=abab6.5s-chat
OPENAI_API_KEY=your-minimax-api-key

# 或其他兼容平台（如 DeepSeek、Moonshot 等）
```

### 2. 本地运行 CLI 工具

```bash
# 克隆项目
git clone https://github.com/catcherxiao/article_jike.git
cd article_jike

# 运行交互模式
python3 main.py

# 或处理文件
python3 main.py -i input/pop_mart_draft.txt -o output/prompt.txt
```

### 3. 启动 Web 界面

```bash
# 方式一：Node.js 本地服务器
node local_server.js
# 访问 http://localhost:3000

# 方式二：Python 简易服务器
python3 -m http.server 8000
# 访问 http://localhost:8000/wechat_workflow.html
```

### 4. Vercel 一键部署

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/catcherxiao/article_jike)

详细部署指南见 [VERCEL_GUIDE.md](./VERCEL_GUIDE.md)

---

## 核心功能

| 功能模块 | 说明 |
|---------|------|
| **🎯 Prompt 生成器** | 根据输入内容自动匹配投资大师语录，生成结构化 System Prompt |
| **📝 文章工作流** | 提供从大纲 → 初稿 → 润色 → 排版的完整写作流程（Web 界面） |
| **📚 语录库** | 内置巴菲特、芒格、段永平、王宁等投资大师经典语录 |
| **🎨 风格化重写** | 用「用户需求—消费场景—商业模式」视角重写内容 |
| **🔧 工具脚本** | Markdown 转微信公众号 HTML、Prompt 渲染等辅助工具 |

核心入口：

- [main.py](./main.py) - CLI Prompt 生成器
- [wechat_workflow.html](./wechat_workflow.html) - Web 写作界面
- [quotes.json](./quotes.json) - 大师语录库
- [tools/](./tools/) - 辅助工具脚本

---

## 项目结构

```text
article_jike/
├── main.py                 # CLI 入口：Prompt 生成器
├── wechat_workflow.html    # Web 界面：完整写作工作流
├── index.html              # 入口跳转页
├── local_server.js         # 本地开发服务器
├── quotes.json             # 投资大师语录库
├── prompts/                # Prompt 模板文件
│   ├── wechat_workflow.md
│   ├── wechat_rewrite_v2.md
│   └── ...
├── tools/                  # 辅助工具
│   ├── md_to_wechat_html.py
│   ├── render_prompt.py
│   └── render_revision_prompt.py
├── api/                    # Vercel Serverless API
│   ├── proxy.js
│   └── status.js
├── input/                  # 输入文件示例
├── output/                 # 输出文件目录
├── samples/                # 示例文章
├── Dockerfile              # Docker 配置
└── vercel.json             # Vercel 配置
```

---

## 部署方式

### 本地部署

```bash
# 运行 CLI 工具
python3 main.py

# 启动本地服务器
node local_server.js
```

### Docker 部署

```bash
# 构建镜像
docker build -t article-jike .

# 运行容器
docker run -p 3000:3000 article-jike
```

### Vercel 部署

```bash
# 安装 Vercel CLI
npm i -g vercel

# 部署
vercel --prod
```

详细部署文档：

- [VERCEL_GUIDE.md](./VERCEL_GUIDE.md) - Vercel 平台部署指南
- [README_DEPLOY.md](./README_DEPLOY.md) - 完整部署文档

---

## 使用场景

- **投资笔记写作**：用价值投资的框架分析公司，生成结构化文章
- **公众号内容创作**：提供从大纲到排版的全流程支持
- **Prompt 工程学习**：学习如何构建高质量的 System Prompt
- **投资智慧整理**：收集和整理投资大师的经典语录和思维方式

---

## 诚实边界

这个项目能做的：

- 用价值投资框架辅助思考和写作
- 自动匹配相关的投资大师语录
- 生成结构化的 System Prompt 供 AI 使用
- 提供完整的文章写作工作流

这个项目做不到的：

- 不能替代专业的投资分析和判断
- 不提供具体的投资建议或买卖时机
- 不能保证生成的内容一定符合价值投资原则
- 语录匹配基于简单关键词，可能不够精准

**一个不告诉你边界在哪的工具，不值得信。**

---

## 参考与致谢

- 投资理念参考：巴菲特、查理·芒格、段永平
- 语录来源：《大道》、《巴菲特致股东的信》、公开采访
- 项目灵感：[duanyongpin.skill](https://github.com/catcherxiao/duanyongpin.skill)

---

<div align="center">

**语录** 只能告诉你他们说过什么。  
**投资智慧回响** 试着帮你用他们的方式思考问题。

<br>

*时间是好公司的朋友，是平庸公司的敌人。*

</div>
