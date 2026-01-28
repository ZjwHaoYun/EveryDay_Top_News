import sys
import random
import asyncio
import logging
from typing import Dict, List, Callable
import json
from crawlers import ALL_ASYNC_CRAWL_FUNCS
from log.mylog import logger
from utils.redis import get_redis_client
from config.config import CACHE_EXPIRE
# 假设你的异步爬虫函数列表已定义（例：[async_get_pengpai_hot, async_get_toutiao_hot, ...]）

async def run_all_crawlers(batch_size: int = 5) -> Dict[str, List[Dict]]:
    """
    执行所有异步爬虫，分批并发控制，返回统一格式字典：{站点名: [热点数据列表]}
    
    Args:
        batch_size: 每批并发请求数，默认 5，避免请求过快被反爬
    
    Returns:
        Dict[str, List[Dict]]: 例如 {"澎湃新闻": [{"hot_label": "...", "hot_url": "...", ...}], ...}
    """
    # Windows系统事件循环兼容（保留原逻辑）
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    redis_client = get_redis_client()
    if redis_client == None:
        logger.error("redis client为空")
        return
    redis_data = redis_client.get("hotnews")
    
    if redis_data != None:
        logger.info("从redis中获取数据")
        return json.loads(redis_data)
        
    all_results: Dict[str, List[Dict]] = {}  # 最终聚合结果，字典初始化
    if not ALL_ASYNC_CRAWL_FUNCS:
        logger.warning("未配置任何异步爬虫函数，ALL_ASYNC_CRAWL_FUNCS 为空")
        return all_results

    # 分批执行爬虫（保留原分批逻辑）
    total_crawlers = len(ALL_ASYNC_CRAWL_FUNCS)
    logger.info(f"开始执行所有爬虫，共{total_crawlers}个，每批并发{batch_size}个")
    
    for i in range(0, total_crawlers, batch_size):
        batch_tasks = ALL_ASYNC_CRAWL_FUNCS[i:i + batch_size]
        batch_num = i // batch_size + 1
        logger.info(f"执行第{batch_num}批爬虫，共{len(batch_tasks)}个")
        
        # 创建异步任务
        tasks = [func() for func in batch_tasks]
        # 并发执行，return_exceptions=True 保证单个爬虫失败不影响整批
        batch_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 处理每批结果（核心修正：异常处理+正确聚合+空数据过滤）
        for idx, result in enumerate(batch_results):
            crawler_func = batch_tasks[idx].__name__  # 获取爬虫函数名，方便日志排查
            # 1. 处理异常：当前爬虫执行失败
            if isinstance(result, Exception):
                logger.error(f"爬虫{crawler_func}执行失败：{str(result)}", exc_info=True)
                continue
            # 2. 校验结果格式：必须是{站点名: 列表}的字典，避免格式错误
            if not isinstance(result, dict) or len(result) == 0:
                logger.warning(f"爬虫{crawler_func}返回格式异常，非有效字典：{result}")
                continue
            # 3. 遍历爬虫返回的站点-数据，过滤空列表，聚合结果
            for source, new_list in result.items():
                # 过滤空数据：无热点的站点不加入结果
                if not isinstance(new_list, list) or len(new_list) == 0:
                    logger.info(f"爬虫{crawler_func}的站点{source}无热点数据，跳过")
                    continue
                # 聚合结果：覆盖式更新（同站点重复爬取取最后一次结果）
                all_results[source] = new_list
                logger.info(f"成功爬取站点{source}，共{len(new_list)}条热点数据")
        
        # 批次间延迟（保留原逻辑，随机2-3秒，避免反爬）
        if i + batch_size < total_crawlers:
            delay = random.uniform(2, 3)
            logger.info(f"第{batch_num}批爬虫执行完成，延迟{delay:.2f}秒执行下一批")
            await asyncio.sleep(delay)

    logger.info(f"所有爬虫执行完成，最终聚合{len(all_results)}个站点的热点数据")
    redis_client.setex(
            "hotnews",
            CACHE_EXPIRE,
            json.dumps(all_results)  # 序列化为JSON字符串
        )
    return all_results