"""
数据模型定义
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict


# ============ 关键词相关 ============

class KeywordExpandRequest(BaseModel):
    seed_keyword: str = Field(..., description="种子关键词", example="猫粮")
    count: int = Field(default=30, ge=1, le=100, description="目标关键词数量")


class KeywordExpandResponse(BaseModel):
    keywords: List[str]
    sources: List[str]
    total: int


# ============ 意图分类相关 ============

class ClassifyRequest(BaseModel):
    keywords: List[str] = Field(..., description="待分类关键词列表")


class ClassifyResponse(BaseModel):
    informational: List[Dict[str, str]] = Field(default_factory=list, description="信息型关键词")
    transactional: List[Dict[str, str]] = Field(default_factory=list, description="交易型关键词")
    navigational: List[Dict[str, str]] = Field(default_factory=list, description="导航型关键词")
    qa: List[Dict[str, str]] = Field(default_factory=list, description="问答型关键词")


# ============ TDK相关 ============

class TDKRequest(BaseModel):
    keyword: str = Field(..., description="核心关键词")
    intent_type: str = Field(default="informational", description="搜索意图类型")
    article_content: Optional[str] = Field(None, description="文章内容（可选）")
    word_count: int = Field(default=500, ge=100, le=3000, description="软文字数")


class TDKResponse(BaseModel):
    title: str = Field(..., description="SEO标题")
    description: str = Field(..., description="Meta描述")
    keywords: List[str] = Field(..., description="关键词列表")
    h1: str = Field(..., description="H1标题")


# ============ 完整SEO包 ============

class SEOGenerateRequest(BaseModel):
    industry: str = Field(..., description="行业关键词", example="猫粮")
    language: str = Field(default="zh-CN", description="语言")
    article_style: str = Field(default="professional", description="文章风格")


class SEOKeyword(BaseModel):
    keyword: str
    search_volume: Optional[str] = None
    competition: Optional[str] = None
    intent: str


class SEOClassified(BaseModel):
    informational: List[SEOKeyword]
    transactional: List[SEOKeyword]
    navigational: List[SEOKeyword]
    qa: List[SEOKeyword]


class SEOGenerateResponse(BaseModel):
    keywords: List[SEOKeyword]
    classified: SEOClassified
    article: Dict
    tdk: TDKResponse
