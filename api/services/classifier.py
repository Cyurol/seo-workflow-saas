"""
搜索意图分类器
"""
import re
from typing import List, Dict, Tuple


class IntentClassifier:
    """
    搜索意图分类器
    
    分类标准：
    - Information（信息型）：用户寻找信息、答案、知识
    - Transactional（交易型）：用户准备购买或有购买意图
    - Navigational（导航型）：用户寻找特定网站/品牌
    - QA（问答型）：用户有具体问题需要回答
    """
    
    # 意图信号词
    INFO_SIGNALS = [
        "how to", "how do", "what is", "what are", "why do", "why is",
        "meaning of", "definition", "difference between", "compare",
        "guide", "tutorial", "tips", "advice", "learn about",
        "原理", "是什么", "怎么", "如何", "为什么", "教程",
        "介绍", "解释", "意思", "区别", "方法", "技巧"
    ]
    
    TRANSACTION_SIGNALS = [
        "buy", "purchase", "order", "price", "cost", "cheap", "discount",
        "coupon", "deal", "best", "top", "review", "compare price",
        "buy now", "order online", "best price",
        "购买", "多少钱", "价格", "优惠", "促销", "打折",
        "哪个好", "推荐", "排行榜", "品牌", "选购", "正品"
    ]
    
    NAVIGATIONAL_SIGNALS = [
        "login", "sign in", "website", "official site", "homepage",
        "官网", "官方网站", "登录", "入口", "网站", "首页"
    ]
    
    QA_SIGNALS = [
        "?", "faq", "question", "answer", "help",
        "吗", "呢", "？", "问答", "常见问题", "解答"
    ]
    
    def classify(self, keywords: List[str]) -> Dict[str, List[Dict[str, str]]]:
        """
        对关键词列表进行意图分类
        
        Returns:
            {
                "informational": [...],
                "transactional": [...],
                "navigational": [...],
                "qa": [...]
            }
        """
        classified = {
            "informational": [],
            "transactional": [],
            "navigational": [],
            "qa": []
        }
        
        for keyword in keywords:
            intent, confidence = self.classify_single(keyword.lower())
            
            result = {
                "keyword": keyword,
                "intent": intent,
                "confidence": confidence
            }
            
            classified[intent].append(result)
        
        return classified
    
    def classify_single(self, keyword: str) -> Tuple[str, float]:
        """
        单个关键词分类
        
        Returns:
            (意图类型, 置信度)
        """
        keyword = keyword.lower().strip()
        
        # 检查导航型
        for signal in self.NAVIGATIONAL_SIGNALS:
            if signal in keyword:
                return "navigational", 0.9
        
        # 检查问答型
        if "?" in keyword or "？" in keyword:
            return "qa", 0.95
        
        for signal in self.QA_SIGNALS:
            if signal in keyword:
                return "qa", 0.8
        
        # 计算各意图得分
        scores = {
            "informational": 0.0,
            "transactional": 0.0,
        }
        
        for signal in self.INFO_SIGNALS:
            if signal in keyword:
                scores["informational"] += 0.3
        
        for signal in self.TRANSACTION_SIGNALS:
            if signal in keyword:
                scores["transactional"] += 0.3
        
        # 长度较长的词倾向于信息型
        if len(keyword) > 15:
            scores["informational"] += 0.2
        
        # 带数字的词倾向于交易型（排行、价格）
        if re.search(r'\d', keyword):
            scores["transactional"] += 0.2
        
        # 选择得分最高的
        if scores["transactional"] > scores["informational"]:
            confidence = min(scores["transactional"], 1.0)
            return "transactional", confidence
        else:
            confidence = min(scores["informational"], 1.0)
            return "informational", max(confidence, 0.5)
    
    def get_primary_intent_distribution(self, classified: Dict) -> Dict[str, float]:
        """获取主要意图分布"""
        total = sum(len(v) for v in classified.values())
        if total == 0:
            return {}
        
        return {
            intent: round(len(keywords) / total * 100, 1)
            for intent, keywords in classified.items()
        }


# 单例
classifier = IntentClassifier()
