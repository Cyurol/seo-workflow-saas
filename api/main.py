"""
SEO Workflow SaaS - FastAPI 核心服务
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

app = FastAPI(
    title="SEO Workflow API",
    description="SEO自动化内容生成工具API",
    version="1.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class HealthResponse(BaseModel):
    status: str
    version: str


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """健康检查"""
    return HealthResponse(status="ok", version="1.0.0")


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "SEO Workflow API",
        "docs": "/docs",
        "version": "1.0.0"
    }


# 延迟导入路由，避免循环导入
@app.on_event("startup")
async def startup_event():
    from api.routers import keywords, classify, tdk, seo_generate
    
    app.include_router(keywords.router, prefix="/api/v1/keywords", tags=["关键词挖掘"])
    app.include_router(classify.router, prefix="/api/v1/classify", tags=["意图分类"])
    app.include_router(tdk.router, prefix="/api/v1/tdk", tags=["TDK生成"])
    app.include_router(seo_generate.router, prefix="/api/v1/seo", tags=["SEO生成"])


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
