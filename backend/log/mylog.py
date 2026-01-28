import logging
import colorlog

# 创建 logger
logger = logging.getLogger('MyApp')
logger.setLevel(logging.DEBUG)

# ------------------- 彩色控制台 Handler -------------------
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# 定义彩色格式
formatter = colorlog.ColoredFormatter(
    '%(asctime)s - %(name)s - %(log_color)s%(levelname)s%(reset)s - %(filename)s:%(lineno)d - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',  # 红字白底
    }
)

console_handler.setFormatter(formatter)

# ------------------- 文件 Handler（无颜色）-------------------
file_handler = logging.FileHandler('app.log', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
)
file_handler.setFormatter(file_formatter)

# 添加 handler
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# 使用
if __name__ == "__main__":
    logger.debug('调试信息，只写入文件')
    logger.info('程序启动')
    logger.warning('内存使用较高')
    logger.error('文件读取失败')
    logger.critical('严重错误！')