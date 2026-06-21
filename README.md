# 🛠️ SEO Workflow SaaS

自动化SEO内容生成工具，输入行业关键词，自动产出完整的SEO内容包。

**完全免费！无需API Key！**

## 📋 功能特性

| 功能 | 描述 |
|------|------|
| 关键词挖掘 | 本地算法智能生成30+长尾关键词 |
| 意图分类 | 信息型/交易型/导航型/问答型 自动分类 |
| SEO软文 | AI智能生成SEO友好文章（需Coze LLM） |
| TDK生成 | 自动生成Title/Description/Keywords |

## 🏗️ 架构

```
用户输入（行业词）
    ↓
Coze Workflow（编排核心 + LLM生成）
    ↓
Python FastAPI（数据处理）
    ├── 本地关键词生成算法
    ├── 意图分类器
    └── TDK生成
```

## 🚀 快速开始

### 1. 安装依赖

```bash
cd seo-workflow-saas/api
pip install -r requirements.txt
```

### 2. 启动服务

```bash
cd api
uvicorn main:app --reload --port 8000
```

### 3. 测试API

```bash
# 健康检查
curl http://localhost:8000/health

# 挖掘关键词
curl -X POST http://localhost:8000/api/v1/keywords/expand \
  -H "Content-Type: application/json" \
  -d '{"seed_keyword": "猫粮", "count": 30}'

# 完整SEO生成
curl -X POST http://localhost:8000/api/v1/seo/generate \
  -H "Content-Type: application/json" \
  -d '{"industry": "猫粮"}'
```

## 📡 API 文档

启动服务后访问: http://localhost:8000/docs

## 🐳 Docker 部署

```bash
docker build -t seo-workflow .
docker run -p 8000:8000 seo-workflow
```

## 🚀 Railway 一键部署

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app)

1. 点击上方按钮或访问 https://railway.app
2. 连接 GitHub 仓库
3. Railway 自动检测 Dockerfile 并部署

## 📁 项目结构

```
seo-workflow-saas/
├── api/                    # Python FastAPI服务
│   ├── main.py            # 入口
│   ├── routers/           # API路由
│   ├── services/          # 业务服务
│   └── models/            # 数据模型
├── workflows/             # Coze Workflow配置
├── docs/                  # 文档
├── Dockerfile            # Docker配置
└── requirements.txt      # 依赖
```

## 🔧 可选配置（高级）

如需使用真实搜索数据，可配置以下环境变量：

```bash
GOOGLE_API_KEY=your_api_key
GOOGLE_SEARCH_ENGINE_ID=your_engine_id
```

不配置也能正常使用！

## 📄 License

MIT
