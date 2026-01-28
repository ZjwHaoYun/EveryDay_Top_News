from pydantic import BaseModel, EmailStr, Field


from typing import List, Dict

class HotTopic(BaseModel):
    hot_label: str = Field(..., description="热点标题 / 标签")
    hot_url: str = Field(..., description="热点链接，http/https 开头")
    hot_value: str = Field(..., description="热度值 / 指数，没有设为0")

    class Config:
        extra = "forbid"
        title = "HotTopic"

# 核心微调：hot_topics为 平台名: HotTopic对象列表 的字典，贴合爬虫返回结构
class HotTopics(BaseModel):
    hot_topics: Dict[str, List[HotTopic]] = Field(..., description="各平台热点集合，key=平台名，value=热点对象列表")

    class Config:
        extra = "forbid"
        title = "HotTopics"