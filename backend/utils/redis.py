
import redis
from config.config import REQUEST_TIMEOUT,REDIS_DB,REDIS_HOST,REDIS_PORT
from log.mylog import logger

def get_redis_client():
    # 初始化Redis客户端
    redis_client = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        decode_responses=True  # 自动解码返回值为字符串
    )
    logger.info(f"redis_client:{redis_client}")
    return redis_client
