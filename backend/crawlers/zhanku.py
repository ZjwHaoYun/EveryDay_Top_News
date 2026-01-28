import sys
import logging
from pathlib import Path
import asyncio
# 路径配置
parent_path = Path(__file__).parent.parent
sys.path.append(str(parent_path))


from utils.async_template import async_fetch
from utils.parse import parse_tencent_news
from utils.parse import parse_zhanku

# 记得导入你的async_fetch、parse_tencent_news函数
# from 你的文件 import async_fetch, parse_tencent_news

async def get_zhanku_data():
    
    url = "https://www.zcool.com.cn/p1/ranking/list"
    params = {
        "p": 1,
        "ps": 20,
        "rank_id": 351,
        "type": 3
    }
    data =  await async_fetch(crawl_name="zhanku",url= url,params=params)
    
    return data


if __name__ == "__main__":
    # 核心：用asyncio.run()启动异步函数
    # 增加try-except捕获异常，方便调试（比如接口请求失败、解析失败）
    try:
        res = asyncio.run(get_zhanku_data())
        print("腾讯热点数据获取成功：")
        print(res)  # 打印返回的结果，验证数据是否正确
    except Exception as e:
        print(f"测试失败，报错信息：{type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()  # 打印详细的报错堆栈，定位问题行

    