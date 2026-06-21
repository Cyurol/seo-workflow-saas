"""
SEO完整生成路由 - 整合所有步骤
"""
from fastapi import APIRouter
from api.models.schemas import (
    SEOGenerateRequest, SEOGenerateResponse, SEOKeyword,
    SEOClassified, TDKResponse
)
from api.services.google_search import keyword_generator
from api.services.classifier import classifier

router = APIRouter()


@router.post("/generate", response_model=SEOGenerateResponse)
async def generate_seo_package(request: SEOGenerateRequest):
    """
    生成完整SEO内容包
    
    完整流程（纯本地算法）：
    1. 关键词挖掘（本地算法）
    2. 意图分类
    3. 生成SEO软文（由Coze Workflow调用LLM完成）
    4. 生成TDK标签
    """
    industry = request.industry
    
    # Step 1: 挖掘关键词（本地算法）
    keywords = keyword_generator.expand_keywords(industry, 30)
    
    # 转换为SEOKeyword对象
    seo_keywords = [SEOKeyword(keyword=kw, intent="mixed") for kw in keywords]
    
    # Step 2: 意图分类
    classified_dict = classifier.classify(keywords)
    
    classified = SEOClassified(
        informational=[SEOKeyword(keyword=k["keyword"], intent="informational") 
                      for k in classified_dict["informational"]],
        transactional=[SEOKeyword(keyword=k["keyword"], intent="transactional") 
                      for k in classified_dict["transactional"]],
        navigational=[SEOKeyword(keyword=k["keyword"], intent="navigational") 
                     for k in classified_dict["navigational"]],
        qa=[SEOKeyword(keyword=k["keyword"], intent="qa") 
            for k in classified_dict["qa"]]
    )
    
    # Step 3: TDK生成（基于主意图）
    distribution = classifier.get_primary_intent_distribution(classified_dict)
    primary_intent = max(distribution, key=distribution.get) if distribution else "informational"
    
    tdk = TDKResponse(
        title=f"{industry}专业指南_{industry}推荐评测",
        description=f"专业{industry}资讯平台，提供最新{industry}推荐、权威评测与选购指南，帮您找到最适合的{industry}。",
        keywords=[industry, f"{industry}推荐", f"{industry}评测", f"{industry}排行榜", f"{industry}选购"],
        h1=f"{industry}专业推荐指南"
    )
    
    # Step 4: 文章结构（内容由Coze LLM生成）
    article = {
        "outline": [
            f"{industry}基础知识介绍",
            f"{industry}选购要点",
            f"{industry}热门推荐",
            f"{industry}常见问题解答"
        ],
        "word_count": "1500",
        "style": request.article_style,
        "note": "文章正文由Coze LLM根据关键词生成"
    }
    
    return SEOGenerateResponse(
        keywords=seo_keywords,
        classified=classified,
        article=article,
        tdk=tdk
    )


@router.get("/status")
async def check_service_status():
    """检查服务状态"""
    return {
        "status": "online",
        "services": {
            "keyword_generator": "available",
            "classifier": "available"
        },
        "mode": "local_algorithm"
    }
