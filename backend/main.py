import sys
import logging
from pathlib import Path
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
# 导入模型
from model.hotnew import HotTopic, HotTopics
# 导入爬虫执行器
from utils.crawler_executor import run_all_crawlers

# 路径配置
parent_path = Path(__file__).parent.parent
sys.path.append(str(parent_path))

app = FastAPI(title="热点爬虫 API")
origins = [
    "*",  # 允许所有前端域名请求，开发环境用
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 允许的源（前端域名）
    allow_credentials=True,  # 允许携带Cookie（如需前端传Cookie则开启）
    allow_methods=["*"],  # 允许所有HTTP方法（GET/POST/PUT/DELETE等）
    allow_headers=["*"],  # 允许所有请求头（Content-Type/Token等）
)

# 接口统一响应模型
class newsResponse(BaseModel):
    code: int = Field(200, description="业务状态码，200为成功")
    message: str = Field("success", description="接口提示信息")
    data: HotTopics = Field(..., description="各平台热点数据")

    class Config:
        extra = "forbid"

@app.get("/api/hot-topics", response_model=newsResponse)
async def get_hot_topics():
    print("进入 get_hot_topics函数")
    try:
        # 1. 调用执行器，聚合所有爬虫结果：{平台名1: [字典列表], 平台名2: [字典列表], ...}
        # 例：{'澎湃新闻': [...], '今日头条': [...]}
        raw_results = await run_all_crawlers()
        
        # 2. 初始化空字典，用来组装「平台名: HotTopic对象列表」
        hot_topic_dict = {}
        for platform_name, topic_dict_list in raw_results.items():
            # 存放当前平台的HotTopic对象
            platform_topic_list = []
            for topic_dict in topic_dict_list:
                # 关键：将字典转HotTopic对象，自动校验字段/类型
                # 自动把hot_value的数字0转成字符串"0"，匹配模型要求
                topic_obj = HotTopic(**topic_dict)
                platform_topic_list.append(topic_obj)
            # 把当前平台的HotTopic对象列表存入字典
            hot_topic_dict[platform_name] = platform_topic_list
        
        # 3. 实例化HotTopics模型，传入组装好的字典
        hot_topics_data = HotTopics(hot_topics=hot_topic_dict)
        
        # 4. 实例化统一响应模型并返回，FastAPI自动序列化JSON
        return newsResponse(
            code=200,
            message="success",
            data=hot_topics_data
        )
    
    except Exception as e:
        logging.exception("爬取失败")
        raise HTTPException(status_code=500, detail=f"爬取失败：{str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="0.0.0.0",
        port=8001,
        reload=True
    )