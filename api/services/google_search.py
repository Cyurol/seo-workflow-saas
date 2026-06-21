"""
本地关键词挖掘服务 - 无需API Key
"""
import re
from typing import List, Set


class KeywordGenerator:
    """
    本地关键词挖掘 - 纯算法实现
    
    策略：
    1. 语义扩展 - 根据行业词类型扩展相关词
    2. 搜索意图词缀 - 添加信息型/交易型词缀
    3. 长尾组合 - 生成常见搜索组合模式
    """
    
    # 信息型词缀
    INFO_SUFFIXES = [
        "是什么", "怎么", "如何", "为什么", "教程", "指南", "方法",
        "原理", "介绍", "解释", "意思", "区别", "技巧", "窍门",
        "常见问题", "FAQ", "问答", "知识", "概念", "定义"
    ]
    
    # 交易型词缀
    TRANSACTION_SUFFIXES = [
        "推荐", "排行榜", "评测", "哪个好", "十大", "品牌",
        "价格", "多少钱", "优惠", "折扣", "选购", "攻略",
        "对比", "比较", "性价比", "平替", "替代", "替代品",
        "正品", "辨别", "真伪", "二手", "租赁"
    ]
    
    # 修饰词前缀
    MODIFIERS = [
        "十大", "最佳", "最好", "最新", "2024", "2025", "专业",
        "平价", "高端", "入门", "新手", "小白", "评测",
        "真实", "客观", "良心", "推荐", "避坑", "必买"
    ]
    
    # 常见搜索模式
    SEARCH_PATTERNS = [
        "{seed}", "{seed} {suffix}", "{modifier} {seed}",
        "{modifier} {seed} {suffix}", "{seed} vs {seed}",
        "{seed} 好不好", "{seed} 有用吗", "{seed} 怎么样",
        "如何选择 {seed}", "{seed} 使用注意事项"
    ]
    
    # 行业分类关键词库
    INDUSTRY_KEYWORDS = {
        "科技": ["手机", "电脑", "平板", "笔记本", "耳机", "音箱", "相机", "游戏机", "智能手表", "无人机"],
        "数码": ["手机", "电脑", "平板", "相机", "耳机", "键盘", "鼠标", "显示器", "固态硬盘", "内存条"],
        "生活": ["零食", "饮料", "调味品", "厨具", "家居", "床上用品", "收纳", "清洁", "收纳", "日用"],
        "美妆": ["护肤品", "化妆品", "香水", "口红", "粉底", "眼影", "面膜", "面霜", "精华", "防晒"],
        "服装": ["T恤", "裤子", "裙子", "外套", "鞋子", "包包", "帽子", "围巾", "袜子", "内衣"],
        "电器": ["冰箱", "洗衣机", "空调", "电视", "油烟机", "扫地机器人", "吸尘器", "电饭煲", "破壁机", "空气炸锅"],
        "宠物": ["猫粮", "狗粮", "猫砂", "宠物玩具", "宠物窝", "宠物笼", "宠物背包", "宠物零食", "宠物沐浴露", "宠物牵引绳"],
        "母婴": ["奶粉", "纸尿裤", "婴儿车", "婴儿床", "奶瓶", "辅食", "婴儿服装", "儿童玩具", "儿童安全座椅", "妈咪包"],
        "运动": ["跑步鞋", "运动服", "瑜伽垫", "哑铃", "健身卡", "游泳装备", "骑行装备", "登山装备", "羽毛球拍", "乒乓球拍"],
        "户外": ["帐篷", "睡袋", "登山包", "露营灯", "折叠椅", "烧烤架", "渔具", "帐篷", "冲锋衣", "登山鞋"]
    }
    
    def __init__(self):
        self._load_custom_suffixes()
    
    def _load_custom_suffixes(self):
        """加载额外的行业特定词缀"""
        # 可以从数据库或配置文件加载
        pass
    
    def expand_keywords(self, seed_keyword: str, count: int = 30) -> List[str]:
        """
        扩展关键词
        
        Args:
            seed_keyword: 种子关键词，如"猫粮"
            count: 目标关键词数量
            
        Returns:
            扩展后的关键词列表
        """
        keywords = set()
        
        # 1. 添加种子词本身
        keywords.add(seed_keyword)
        
        # 2. 识别行业类型并添加行业相关词
        industry_keywords = self._get_industry_keywords(seed_keyword)
        
        # 3. 生成信息型关键词
        for suffix in self.INFO_SUFFIXES:
            if len(keywords) >= count:
                break
            keywords.add(f"{seed_keyword}{suffix}")
        
        # 4. 生成交易型关键词
        for suffix in self.TRANSACTION_SUFFIXES:
            if len(keywords) >= count:
                break
            keywords.add(f"{seed_keyword}{suffix}")
        
        # 5. 生成修饰词组合
        for modifier in self.MODIFIERS:
            if len(keywords) >= count:
                break
            keywords.add(f"{modifier} {seed_keyword}")
        
        # 6. 生成搜索模式组合
        for pattern in self.SEARCH_PATTERNS:
            if len(keywords) >= count:
                break
            keyword = pattern.replace("{seed}", seed_keyword)
            keywords.add(keyword)
        
        # 7. 行业特定扩展
        for related in industry_keywords:
            if len(keywords) >= count:
                break
            if related != seed_keyword:
                keywords.add(f"{seed_keyword} {related}")
                keywords.add(f"{related} {seed_keyword}")
        
        # 8. 问答型关键词
        questions = [
            f"{seed_keyword}哪个牌子好",
            f"{seed_keyword}怎么选",
            f"{seed_keyword}多少钱",
            f"{seed_keyword}有用吗",
            f"{seed_keyword}效果如何",
            f"{seed_keyword}注意事项",
            f"{seed_keyword}和什么的区别",
            f"新手怎么选{seed_keyword}",
            f"{seed_keyword}选购要点",
            f"{seed_keyword}避坑指南"
        ]
        keywords.update(questions[:count - len(keywords)] if len(keywords) < count else [])
        
        # 9. 添加同类型产品的对比词
        for related in industry_keywords[:3]:
            if len(keywords) >= count:
                break
            if related != seed_keyword:
                keywords.add(f"{seed_keyword} vs {related}")
        
        return list(keywords)[:count]
    
    def _get_industry_keywords(self, seed: str) -> List[str]:
        """获取同行业相关关键词"""
        seed_lower = seed.lower()
        
        # 遍历行业词库
        for industry, words in self.INDUSTRY_KEYWORDS.items():
            for word in words:
                if word in seed_lower or seed_lower in word:
                    return words
        
        # 如果没找到匹配，返回通用词
        return [
            "推荐", "评测", "排行榜", "品牌", "价格",
            "选购", "攻略", "对比", "哪个好", "新手"
        ]
    
    def get_keyword_metrics(self, keyword: str) -> dict:
        """
        估算关键词指标（模拟数据）
        
        实际项目中可以接入百度指数、Google Trends等API
        """
        import random
        
        # 估算搜索量（基于关键词长度和类型）
        base_volume = random.randint(100, 10000)
        if any(suffix in keyword for suffix in ["推荐", "排行榜", "评测"]):
            volume = int(base_volume * 1.5)
        elif any(suffix in keyword for suffix in ["教程", "怎么", "如何"]):
            volume = int(base_volume * 0.8)
        else:
            volume = base_volume
        
        # 估算竞争度
        if any(word in keyword for word in ["十大", "排行榜", "评测"]):
            competition = "中"
        elif len(keyword) > 10:
            competition = "低"
        else:
            competition = "高"
        
        return {
            "keyword": keyword,
            "estimated_volume": volume,
            "competition": competition,
            "difficulty": random.randint(30, 90) if competition == "高" else random.randint(10, 50)
        }


# 单例
keyword_generator = KeywordGenerator()
