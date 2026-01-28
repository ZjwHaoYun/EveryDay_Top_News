from utils.async_template import async_fetch

async def async_get_toutiao_hot():
    """澎湃新闻热榜爬虫"""
    url = "https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc"
    data =  await async_fetch(crawl_name="toutiao_hot", url=url)
    if "data" in data:
        data = data['data']
    result = []
    for item in data:
        hot_value = int(item["HotValue"])
        hot_url = item["Url"]
        hot_label = item["Title"]
        result.append({
            "hot_value": str(hot_value),
            "hot_url": hot_url,
            "hot_label": hot_label
        })
    result.sort(key=lambda x: int(x["hot_value"]), reverse=True)
    return {'今日头条':result}


   