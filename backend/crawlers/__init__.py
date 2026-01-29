from .pengpai import async_get_pengpai_hot
from .toutiao import async_get_toutiao_hot
from .baidu import get_baidu_data
from .juejin import get_juejin_hot
from  .baijingchuhai import get_baijingchuhai_data
from .csdn import get_csdn_data
from .acFun import get_acfun_data
from .diyicaijing import get_diyicaijing_data
from .zhihu import  get_zhihu_data
from .douban_movie import get_douban_movie_data
from .dongchedi import get_dongchedi_data

# 汇总所有异步爬虫函数（主文件直接用这个列表）
ALL_ASYNC_CRAWL_FUNCS = [
    async_get_pengpai_hot,
    async_get_toutiao_hot,
    get_baidu_data,
    get_juejin_hot,
    get_baijingchuhai_data,
    get_csdn_data,
    get_acfun_data,
    get_diyicaijing_data,
    get_zhihu_data,
    get_douban_movie_data,
    get_dongchedi_data
  
]

