from pathlib import Path
import sys
parent_path = Path(__file__).parent.parent
sys.path.append(str(parent_path))

import requests
from urllib.parse import urljoin
from utils.async_template import async_fetch
import asyncio

async def get_zhihu_data() -> None:
    
    # 发送请求
    url = 'https://api.zhihu.com/topstory/hot-list'
    response = await async_fetch(crawl_name='知乎',url=url)
    items = response['data']
    result = []
    # 遍历全部热榜，取出几个属性
    for rank, item in enumerate(items, start=1):
        target = item.get('target')
        title = target.get('title')
        hot = item.get('detail_text').split(' ')[0]
        question_url = target.get('url').replace(
            'api', 'www').replace('questions', 'question')
       
        result.append({
            #"rank": str(rank),      # 排名
            "hot_label": title,  # 处理后的标题
            "hot_url":  question_url ,       # 新闻链接
            "hot_value": str(hot) #热度
        })
        
    result.sort(key=lambda x: int(x["hot_value"]), reverse=True)
    
    return {"知乎":result}
    
# async def get_zhihu_data() -> None:
#     # 请求头
#     headers = {

#         'User-Agent': 'osee2unifiedRelease/4318 osee2unifiedReleaseVersion/7.7.0 Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
#         'Host': 'api.zhihu.com',
#     }
#     # 请求参数
#     params = (
#         ('limit', '50'),
#         ('reverse_order', '0'),
#     )
#     # 发送请求
#     response = requests.get(
#         'https://api.zhihu.com/topstory/hot-list', headers=headers, params=params)
#     print(response.json())

#     items = response.json()['data']
#     print(items)
#     result = []
#     # 遍历全部热榜，取出几个属性
#     for rank, item in enumerate(items, start=1):
#         target = item.get('target')
#         title = target.get('title')
#         hot = int(item.get('detail_text').split(' ')[0])
#         question_url = target.get('url').replace(
#             'api', 'www').replace('questions', 'question')
#         # 添加到处理结果列表
#         print(type(hot))
#         print(type(rank))
#         result.append({
#             "hot_label": title,  # 处理后的标题
#             "hot_url":  question_url ,       # 新闻链接
#             "hot_value": str(hot) #热度
#         })
        
#     result.sort(key=lambda x: int(x["hot_value"]), reverse=True)
#     return {"知乎":result}
    

if __name__ == "__main__":
    # 核心：用asyncio.run()启动异步函数
    # 增加try-except捕获异常，方便调试（比如接口请求失败、解析失败）
    try:
        res = asyncio.run(get_zhihu_data())
        #res = get_topnews_from_zhihu()
        print("知乎热点数据获取成功：")
        print(res)  # 打印返回的结果，验证数据是否正确
    except Exception as e:
        print(f"测试失败，报错信息：{type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()  # 打印详细的报错堆栈，定位问题行

    