from utils.async_template import async_fetch


async def async_get_pengpai_hot():
    """澎湃新闻热榜爬虫"""
    url = "https://cache.thepaper.cn/contentapi/wwwIndex/rightSidebar"
    data =  await async_fetch(crawl_name="pengpai_hot", url=url)
    data = data['data']['hotNews']
    result = []
    for item in data:
        result.append({
            "hot_label": item['name'],
            "hot_url": "https://www.thepaper.cn/newsDetail_forward_" +item['contId'],
            "hot_value": '0'
        })
    return {'澎湃新闻':result}
   