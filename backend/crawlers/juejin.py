from utils.async_template import async_fetch
async def get_juejin_hot():
    url = "https://api.juejin.cn/content_api/v1/content/article_rank?category_id=1&type=hot"
    data =  await async_fetch(crawl_name="juejin", url=url)

    if "data" in data:
        data = data["data"]
    result = []
    for item in data:
        hot_value = int(item['content_counter']['hot_rank'])
        hot_url = "https://juejin.cn/post/" + str(item["content"]["content_id"])
        hot_label = item["content"]['title']
        result.append({
            "hot_value": str(hot_value),
            "hot_url": hot_url,
            "hot_label": hot_label
        })
    result.sort(key=lambda x: int(x["hot_value"]), reverse=True)
    return {'掘金':result}



    

