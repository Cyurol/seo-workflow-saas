"""
TDK生成路由
"""
from fastapi import APIRouter
from api.models.schemas import TDKRequest, TDKResponse

router = APIRouter()


@router.post("/", response_model=TDKResponse)
async def generate_tdk(request: TDKRequest):
    """
    生成SEO TDK标签
    
    TDK = Title + Description + Keywords
    
    - Title: 页面标题（50-60字符）
    - Description: Meta描述（150-160字符）
    - Keywords: 关键词列表（5-10个）
    - H1: 页面主标题
    """
    keyword = request.keyword
    intent = request.intent_type
    
    # 根据意图生成不同风格的TDK
    if intent == "transactional":
        title = f"{keyword}推荐_{keyword}排行榜_{keyword}哪个好"
        description = f"精选{keyword}推荐，汇集最新{keyword}排行榜，权威{keyword}评测。帮您找到最好的{keyword}，点击查看详细攻略。"
        h1 = f"2024年{keyword}推荐排行榜"
    elif intent == "informational":
        title = f"{keyword}完全指南_{keyword}使用教程"
        description = f"专业{keyword}使用指南，详解{keyword}相关知识与技巧。帮助您全面了解{keyword}，轻松解决各种问题。"
        h1 = f"{keyword}完全指南"
    else:
        title = f"{keyword}_权威{keyword}网站"
        description = f"专业{keyword}资讯平台，提供{keyword}相关内容的详细介绍与最新资讯。"
        h1 = keyword
    
    # 生成关键词列表
    keywords = [
        keyword,
        f"{keyword}推荐",
        f"{keyword}哪个好",
        f"{keyword}评测",
        f"{keyword}攻略",
        f"{keyword}教程",
    ]
    
    # 截断到合适长度
    title = title[:60]
    description = description[:160]
    
    return TDKResponse(
        title=title,
        description=description,
        keywords=keywords,
        h1=h1
    )


@router.post("/batch")
async def generate_tdk_batch(requests: list[TDKRequest]):
    """批量生成TDK"""
    results = []
    for req in requests:
        result = await generate_tdk(req)
        results.append({
            "keyword": req.keyword,
            "tdk": result.model_dump()
        })
    return {"results": results}
