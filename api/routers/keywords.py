"""
关键词挖掘路由
"""
from fastapi import APIRouter
from api.models.schemas import KeywordExpandRequest, KeywordExpandResponse
from api.services.google_search import keyword_generator

router = APIRouter()


@router.post("/expand", response_model=KeywordExpandResponse)
async def expand_keywords(request: KeywordExpandRequest):
    """
    扩展关键词
    
    基于种子关键词，使用本地算法挖掘相关长尾词
    
    策略：
    1. 语义扩展 - 根据行业词类型扩展相关词
    2. 搜索意图词缀 - 添加信息型/交易型词缀
    3. 长尾组合 - 生成常见搜索组合模式
    """
    # 使用本地算法生成关键词
    keywords = keyword_generator.expand_keywords(
        request.seed_keyword, 
        request.count
    )
    
    return KeywordExpandResponse(
        keywords=keywords,
        sources=["local_algorithm"],
        total=len(keywords)
    )


@router.get("/related/{keyword}")
async def get_related_keywords(keyword: str, count: int = 10):
    """获取单个关键词的相关词"""
    keywords = keyword_generator.expand_keywords(keyword, count)
    return {
        "keyword": keyword, 
        "related": keywords[:count],
        "metrics": [keyword_generator.get_keyword_metrics(kw) for kw in keywords[:5]]
    }


@router.get("/metrics/{keyword}")
async def get_keyword_metrics(keyword: str):
    """获取关键词指标（搜索量、竞争度估算）"""
    return keyword_generator.get_keyword_metrics(keyword)


@router.post("/expand-with-metrics", response_model=KeywordExpandResponse)
async def expand_keywords_with_metrics(request: KeywordExpandRequest):
    """
    扩展关键词并返回指标
    
    返回每个关键词的估算搜索量和竞争度
    """
    keywords = keyword_generator.expand_keywords(
        request.seed_keyword, 
        request.count
    )
    
    return KeywordExpandResponse(
        keywords=keywords,
        sources=["local_algorithm"],
        total=len(keywords)
    )
