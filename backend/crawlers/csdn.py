import sys
import logging
from pathlib import Path
import asyncio
# 路径配置
parent_path = Path(__file__).parent.parent
sys.path.append(str(parent_path))


from utils.async_template import async_fetch

from utils.parse import parse_csdn

async def get_csdn_data():
    url = "https://blog.csdn.net/phoenix/web/blog/hot-rank?page=0&pageSize=25&type="
    data =  await async_fetch(crawl_name="csdn",url= url)
    result = await parse_csdn(data)
    return {"csdn":result}

if __name__ == "__main__":
    # 核心：用asyncio.run()启动异步函数
    # 增加try-except捕获异常，方便调试（比如接口请求失败、解析失败）
    try:
        res = asyncio.run(get_csdn_data())
        print("腾讯热点数据获取成功：")
        print(res)  # 打印返回的结果，验证数据是否正确
    except Exception as e:
        print(f"测试失败，报错信息：{type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()  # 打印详细的报错堆栈，定位问题行

    
    
    
    
 
