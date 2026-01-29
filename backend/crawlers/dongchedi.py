import sys
import logging
from pathlib import Path
import asyncio
# 路径配置
parent_path = Path(__file__).parent.parent
sys.path.append(str(parent_path))
from urllib.parse import urljoin
from utils.async_template import async_fetch
from .common import parse_dongchedi

import asyncio

# 解决：city_name=undefined + 同步请求更稳定 + 修复URL拼接 + 规范函数名
async def get_dongchedi_data():
    """爬取懂车帝新闻页热点，解决city_name=undefined问题，同步版稳定无坑"""
    url = "https://www.dongchedi.com/news"
    # 强化请求头：添加referer、升级UA，规避懂车帝反爬（解决请求超时核心）
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "referer": "https://www.dongchedi.com/",  # 新增：添加来源页，降低反爬概率
        "Accept-Language": "zh-CN,zh;q=0.9",      # 新增：指定语言，模拟真实浏览器
        "Connection": "keep-alive"                # 新增：长连接，提升请求速度
    }
    
 
    # 同步请求：requests比aiohttp更稳定，新手无异步坑，超时设为20秒足够
    response = await async_fetch(crawl_name="懂车帝",url=url,headers=headers)
    return await parse_dongchedi(response)
    
   
# 主执行入口（直接运行该脚本即可获取结果）
if __name__ == "__main__":
    # 核心：用asyncio.run()启动异步函数
    # 增加try-except捕获异常，方便调试（比如接口请求失败、解析失败）
    try:
        res = asyncio.run(get_dongchedi_data())
        print("腾讯热点数据获取成功：")
        print(res)  # 打印返回的结果，验证数据是否正确
    except Exception as e:
        print(f"测试失败，报错信息：{type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()  # 打印详细的报错堆栈，定位问题行

