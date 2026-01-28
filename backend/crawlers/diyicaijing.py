from pathlib import Path
import sys
parent_path = Path(__file__).parent.parent
sys.path.append(str(parent_path))

import requests
from urllib.parse import urljoin
from utils.async_template import async_fetch
import asyncio
async def get_diyicaijing_data():
    url = "https://www.yicai.com/api/ajax/getranklistbykeys?keys=newsRank%2CvideoRank%2CimageRank%2CliveRank"
    res = await async_fetch(crawl_name='第一财经',url=url)
    hot_data = []
    newsRank = res.get('newsRank', [])
    for news in newsRank.get('week', []):
        title = news['NewsTitle']
        link = urljoin(url, news['url'])
        hotScore = 0
        hot_data.append({
            'hot_label': title,
            'hot_url': link,
            'hot_value': str(hotScore)
        })
    return {"第一财经": hot_data}


if __name__ == "__main__":
    # 核心：用asyncio.run()启动异步函数
    # 增加try-except捕获异常，方便调试（比如接口请求失败、解析失败）
    try:
        res = asyncio.run(get_diyicaijing_data())
        print("腾讯热点数据获取成功：")
        print(res)  # 打印返回的结果，验证数据是否正确
    except Exception as e:
        print(f"测试失败，报错信息：{type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()  # 打印详细的报错堆栈，定位问题行

    