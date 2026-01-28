import requests
import pyquery
from urllib.parse import urljoin
from utils.async_template import async_fetch

async def get_baijingchuhai_data():
    url = "https://www.baijing.cn/newsflashes_txzq/"
    res = await async_fetch(crawl_name="白鲸出海",url=url)
    doc = pyquery.PyQuery(res)
    items = doc("#content_ul>li").items()
    data = []
    for item in items:
        title = item.find("h3>a").text()
        link = item.find("h3>a").attr("href")
        link = urljoin(url, link)
        hotScore = 0
        data.append({
            "hot_label": title,
            "hot_url": link,
            "hot_value": str(hotScore)
        })
    return {"白鲸出海": data}

if __name__ == "__main__":
    print(get_baijingchuhai_data())
    
    
    
 




    