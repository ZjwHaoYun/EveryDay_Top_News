from curl_cffi import requests
import pyquery
from urllib.parse import urljoin
import json
import math
def get_linuxdo_data():
    url = "https://linux.do/top"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }
    res = requests.get(url, headers=headers, timeout=30, impersonate="chrome")
    doc = pyquery.PyQuery(res.text)
    json_data = json.loads(json.loads(doc("discourse-assets-json>div").attr("data-preloaded"))['topic_list'])['topic_list']['topics']

    result = []
    weight_posts = 1.0
    weight_replies = 1.5
    weight_views = 0.5
    weight_likes = 2.0
    for item in json_data:
        posts_count = item.get("posts_count", 0)
        reply_count = item.get("reply_count", 0)
        views_count = item.get("views", 0)
        like_count = item.get("like", 0)
        heat_score = (
            weight_posts * posts_count +
            weight_replies * reply_count +
            weight_views * math.log(views_count + 1) +
            weight_likes * like_count
        )
        result.append({
            "hot_label": item['title'],
            "hot_url": "https://linux.do/t/topic/" + str(item['id']),
            "hot_value": math.floor(heat_score)
        })
    result.sort(key=lambda x: x["hot_value"], reverse=True)
  
    
    return {"linuxdo":json_data}


if __name__=="__main__":
    get_linuxdo_data()
