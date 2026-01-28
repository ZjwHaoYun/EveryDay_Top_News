from config.config import COMMON_HEADERS, REQUEST_TIMEOUT

import logging
import random
import asyncio
from tenacity import retry, stop_after_attempt, wait_random_exponential, retry_if_exception_type
# 核心：导入curl-cffi的异步模块，替代aiohttp
from curl_cffi.requests import AsyncSession
import asyncio
import random
import logging
import json

logger = logging.getLogger(__name__)

def async_retry_decorator():
    return retry(
        stop=stop_after_attempt(5),
        wait=wait_random_exponential(multiplier=1, max=10),
        retry=retry_if_exception_type((Exception,)),
        reraise=False
    )

#@async_retry_decorator()
# async def async_fetch(crawl_name: str, url: str, is_json: bool = True, headers: dict = None,params: dict = None):
#     """使用 curl_cffi.AsyncSession 实现 impersonate 异步爬虫"""
#     try:
#         async with AsyncSession() as session:
#             # 自动 impersonate Chrome，headers 可覆盖默认值
#             resp = await session.get(
#                 url,
#                 headers=headers or {**COMMON_HEADERS},
#                 impersonate="chrome",  # 关键：启用浏览器指纹模拟
#                 timeout=30,
#                 params=params  # 核心：传递查询参数，框架自动拼接、编码
#             )
            
#             await asyncio.sleep(random.uniform(0.5, 2))
            
#             if resp.status_code != 200:
#                 raise Exception(f"HTTP {resp.status_code}")
                
#             data = resp.json() if is_json else resp.text
#             logger.info(f"异步爬取成功：{crawl_name}")
#             return  data
            
#     except Exception as e:
#         logger.error(f"异步爬取失败：{crawl_name} - {e}")
#         return (crawl_name, None)

@async_retry_decorator()
async def async_fetch(
    crawl_name: str, 
    url: str, 
    headers: dict = None,
    params: dict = None,
    timeout: int = 30,
    random_sleep: bool = True  # 可选：是否开启随机休眠防反爬
):
    """
    使用 curl_cffi.AsyncSession 实现异步爬虫，自动识别返回内容是否为JSON
    
    参数说明：
    - crawl_name: 爬虫名称（用于日志标识）
    - url: 目标URL
    - headers: 自定义请求头（覆盖COMMON_HEADERS）
    - params: URL查询参数（字典格式，自动拼接编码）
    - timeout: 请求超时时间（默认30秒）
    - random_sleep: 是否随机休眠0.5-2秒（默认开启，防反爬）
    
    返回值：
    - 成功：(crawl_name, 解析后的数据) → 数据为dict/list（JSON）或str（非JSON）
    - 失败：(crawl_name, None)
    """
    try:
        async with AsyncSession() as session:
            # 合并请求头（自定义头覆盖通用头）
            final_headers ={**COMMON_HEADERS}
            if headers:
                final_headers.update(headers)
            print(final_headers)
            # 发送GET请求
            resp = await session.get(
                url,
                headers=final_headers,
                impersonate="chrome",  # 模拟Chrome浏览器指纹
                timeout=timeout,
                params=params
            )
            
            # 随机休眠（防反爬）
            if random_sleep:
                await asyncio.sleep(random.uniform(0.5, 2))
            
            # 校验HTTP状态码
            if resp.status_code != 200:
                raise Exception(f"HTTP请求失败，状态码：{resp.status_code}")
            
            # 读取原始文本（自动处理编码，优先从响应头获取编码）
            raw_text = resp.text
            if not raw_text:  # 空内容处理
                logger.warning(f"{crawl_name} - 返回内容为空")
                return (crawl_name, "")
            
            # 核心逻辑：自动识别并解析JSON
            try:
                # 尝试解析JSON（兼容各种JSON格式，包括带BOM、多余空格的情况）
                json_data = json.loads(raw_text.strip())
                logger.info(f"异步爬取成功（JSON格式）：{crawl_name}")
                return json_data
            except (json.JSONDecodeError, TypeError, ValueError):
                # 非JSON格式，直接返回原始文本
                logger.info(f"异步爬取成功（文本/HTML格式）：{crawl_name}")
                return raw_text
                
    except Exception as e:
        logger.error(f"异步爬取失败：{crawl_name} - {str(e)}")
        return (crawl_name, None)