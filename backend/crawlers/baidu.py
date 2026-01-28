#coding=utf-8
# 百度热搜
# 路径配置
from pathlib import Path
import sys
parent_path = Path(__file__).parent.parent
sys.path.append(str(parent_path))

from curl_cffi import requests
import pyquery
import re
import json
from utils.async_template import async_fetch
import asyncio
async def get_baidu_data():
    url = "https://top.baidu.com/board?tab=realtime"
    response = await async_fetch(crawl_name="baidu",url=url)
    #需要把这个字符串转换成可解析的 HTML DOM 对象（比如用 pyquery/BeautifulSoup）
    doc = pyquery.PyQuery(response)
    # search_tabs_data = doc("#sanRoot").html()
    search_tabs = re.findall("<!--s-data:(.*?)-->", response, re.S)
    hot_data = []
    if len(search_tabs) > 0:
        search_tabs = json.loads(search_tabs[0])
        datas = search_tabs['data']['cards'][0]['content']
        for data in datas:
            url = data['appUrl']
            title = data['word']
            hotScore = data['hotScore']
            hot_data.append({
                "hot_url": url,
                "hot_label": title,
                "hot_value": str(hotScore)
            })
    return {"百度": hot_data}


if __name__ == "__main__":
    try:
        res = asyncio.run(get_baidu_data())
        print("腾讯热点数据获取成功：")
        print(res)  # 打印返回的结果，验证数据是否正确
    except Exception as e:
        print(f"测试失败，报错信息：{type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()  # 打印详细的报错堆栈，定位问题行
    
