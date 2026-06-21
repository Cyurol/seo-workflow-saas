"""
意图分类路由
"""
from fastapi import APIRouter
from api.models.schemas import ClassifyRequest, ClassifyResponse
from api.services.classifier import classifier

router = APIRouter()


@router.post("/", response_model=ClassifyResponse)
async def classify_keywords(request: ClassifyRequest):
    """
    关键词意图分类
    
    将关键词分类为：
    - informational: 信息型（用户寻找信息）
    - transactional: 交易型（用户有购买意图）
    - navigational: 导航型（用户寻找特定网站）
    - qa: 问答型（用户有具体问题）
    """
    classified = classifier.classify(request.keywords)
    
    return ClassifyResponse(
        informational=classified["informational"],
        transactional=classified["transactional"],
        navigational=classified["navigational"],
        qa=classified["qa"]
    )


@router.get("/distribution")
async def get_intent_distribution(keywords: str):
    """
    获取关键词的意图分布统计
    
    Query参数 keywords: 逗号分隔的关键词列表
    """
    keyword_list = [k.strip() for k in keywords.split(",") if k.strip()]
    
    if not keyword_list:
        return {"error": "请提供关键词列表"}
    
    classified = classifier.classify(keyword_list)
    distribution = classifier.get_primary_intent_distribution(classified)
    
    return {
        "total_keywords": len(keyword_list),
        "distribution": distribution,
        "classified": classified
    }
