
from typing import List, Dict, Any
from .common import parse_douban_movie
import asyncio
from utils.async_template import async_fetch

# 核心爬虫函数（对应原TS的GET异步函数）
async def get_douban_movie_data() -> Dict[str, Any]:
    """爬取豆瓣电影新片榜，返回和原接口一致的JSON结构"""
    # 豆瓣电影新片榜官方地址
    url = "https://movie.douban.com/chart/"
    
    response = await async_fetch(crawl_name='豆瓣电影',url=url)
    result = await parse_douban_movie(response)
    
    return {"豆瓣电影":result}
    
    
# 主执行入口（直接运行该脚本即可获取结果）
if __name__ == "__main__":
    # 核心：用asyncio.run()启动异步函数
    # 增加try-except捕获异常，方便调试（比如接口请求失败、解析失败）
    try:
        res = asyncio.run(get_douban_movie_data())
        print("腾讯热点数据获取成功：")
        print(res)  # 打印返回的结果，验证数据是否正确
    except Exception as e:
        print(f"测试失败，报错信息：{type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()  # 打印详细的报错堆栈，定位问题行

