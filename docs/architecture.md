# SEO Workflow SaaS 工具架构设计

## 📋 项目概述
自动化SEO内容生成工具，输入行业关键词，自动产出完整的SEO内容包。

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────────────┐
│                        Coze Workflow                            │
│  (编排核心 + 用户交互 + 软文生成)                                │
└─────────────────────────┬───────────────────────────────────────┘
                          │ API 调用
                          ↓
┌─────────────────────────────────────────────────────────────────┐
│                   Python FastAPI 服务                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐    │
│  │  关键词挖掘   │  │  意图分类    │  │   TDK生成           │    │
│  │  (Google+    │  │  (信息型/    │  │   (Title/Desc/      │    │
│  │   百度)      │  │   交易型/    │  │    Keywords)        │    │
│  │              │  │   问答型)    │  │                     │    │
│  └──────────────┘  └──────────────┘  └──────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

## 🔌 API 接口设计

### 1. 关键词挖掘
```
POST /api/v1/keywords/expand
Body: { "seed_keyword": "猫粮", "count": 30 }
Response: { "keywords": [...], "sources": ["google", "baidu"] }
```

### 2. 意图分类
```
POST /api/v1/keywords/classify
Body: { "keywords": [...] }
Response: { "informational": [...], "transactional": [...], "navigational": [...] }
```

### 3. TDK生成
```
POST /api/v1/content/tdk
Body: { "keyword": "...", "intent_type": "...", "article_content": "..." }
Response: { "title": "...", "description": "...", "keywords": [...] }
```

### 4. 完整SEO包
```
POST /api/v1/seo/generate
Body: { "industry": "猫粮" }
Response: { "keywords": [...], "classified": {...}, "article": "...", "tdk": {...} }
```

## 🔍 数据源

| 数据源 | 用途 | API |
|--------|------|-----|
| Google Custom Search | 搜索结果分析、相关词挖掘 | Google API Key |
| 百度搜索联想 | 中文长尾词扩展 | 百度搜索开放API |

## 📁 项目结构

```
seo-workflow-saas/
├── api/
│   ├── main.py              # FastAPI入口
│   ├── routers/
│   │   ├── keywords.py      # 关键词挖掘API
│   │   ├── classify.py     # 意图分类API
│   │   └── tdk.py          # TDK生成API
│   ├── services/
│   │   ├── google_search.py # Google搜索服务
│   │   ├── baidu_search.py  # 百度搜索服务
│   │   └── classifier.py    # 意图分类器
│   └── models/
│       └── schemas.py        # 数据模型
├── workflows/
│   └── seo_workflow.json    # Coze Workflow配置
├── docs/
│   └── api_docs.md          # API文档
└── requirements.txt         # Python依赖
```

## 🚀 部署方式

1. **Python API**：部署到云服务器/VPS
2. **Coze Workflow**：导入JSON配置，创建Bot调用API
3. **域名绑定**：API服务公网访问

## 🔐 环境变量

```bash
GOOGLE_API_KEY=        # Google Custom Search API Key
GOOGLE_SEARCH_ENGINE_ID=  # Google搜索引擎ID
BAIDU_API_KEY=         # 百度搜索API Key（可选）
DATABASE_URL=          # 数据库连接（可选，用于缓存）
```
