"""
搜索联想词服务 - 本地算法实现
"""
from typing import List


class SuggestionGenerator:
    """
    搜索联想词生成器 - 纯本地算法
    
    生成常见的搜索联想词模式
    """
    
    # 常见搜索联想词模板
    SUGGESTION_PATTERNS = [
        "{keyword}",
        "{keyword} 推荐",
        "{keyword} 哪个好",
        "{keyword} 排行榜",
        "{keyword} 评测",
        "{keyword} 价格",
        "{keyword} 选购",
        "{keyword} 攻略",
        "{keyword} 对比",
        "{keyword} 区别",
        "{keyword} 知乎",
        "{keyword} 怎么样",
        "{keyword} 好用吗",
        "{keyword} 多少钱",
        "{keyword} 品牌",
        "{keyword} 2024",
        "{keyword} 2025",
        "十大 {keyword}",
        "最佳 {keyword}",
        "如何选购 {keyword}",
        "{keyword} 注意事项",
        "{keyword} 优缺点",
        "{keyword} 使用方法",
        "{keyword} 入门",
        "{keyword} 新手",
        "{keyword} 评测",
        "{keyword} 对比",
        "{keyword} 推荐指数",
        "{keyword} 真实评测",
        "{keyword} 避坑",
        "{keyword} 必买",
        "{keyword} 不推荐",
        "{keyword} 智商税",
        "{keyword} 拔草",
        "{keyword} 种草",
    ]
    
    def get_suggestions(self, keyword: str, count: int = 30) -> List[str]:
        """
        获取搜索联想词
        
        Args:
            keyword: 种子关键词
            count: 目标数量
            
        Returns:
            联想词列表
        """
        suggestions = []
        
        for pattern in self.SUGGESTION_PATTERNS:
            if len(suggestions) >= count:
                break
            suggestion = pattern.replace("{keyword}", keyword)
            suggestions.append(suggestion)
        
        return suggestions


# 单例
suggestion_generator = SuggestionGenerator()
