# 全局请求头
from dotenv import load_dotenv
import os
# 加载环境变量文件
load_dotenv()

COMMON_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}


# 数据库配置
DB_CONFIG = {
    "host": "your_db_host",
    "port": 5432,
    "user": "your_db_user",
    "password": "your_db_pwd",
    "database": "your_db_name"
}

# 超时配置
REQUEST_TIMEOUT = 60  # 单个请求超时（秒）
GLOBAL_TIMEOUT = 60   # 全局超时（秒）

#redis配置
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")  # Redis服务器地址
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))  # Redis端口
REDIS_DB = int(os.getenv("REDIS_DB", 0))  # Redis数据库编号
REDIS_NEWS_KEY = "hot_news"  # Redis中存储新闻的键名
CACHE_EXPIRE = 3600*6  # 缓存过期时间(秒)，1小时

