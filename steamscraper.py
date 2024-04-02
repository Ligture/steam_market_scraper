import time

import bs4
import requests
from bs4 import BeautifulSoup
from requests.cookies import RequestsCookieJar

import assets
import json
from collections import OrderedDict
from plyer import notification


proxy = {
    #'http': 'socks5://127.0.0.1:7890',
    #'https': 'socks5://127.0.0.1:7890'
    # "http": "http://10.10.1.10:3128",
    # "https": "http://10.10.1.10:1080",
}


def scrape(url, query=None, alert='float < 0.18', sortkey=lambda x: x[1]['float']):
    if query is None:
        query = {"start": 0, "count": 10}
    jar = RequestsCookieJar()
    with open("cookie.json", "r") as fp:
        cookie = json.load(fp)
        for i in cookie:
            jar.set(i['name'], i['value'])  # 开始位置  #单页显示数量10 25 50 100
    checkurl = url
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "accept-language": "zh-cn"
    }

    def gethtml():
        global html
        try:
            html = requests.get(checkurl, headers=headers, proxies=proxy, params=query, cookies=jar, timeout=3,
                                verify=False)
        except:
            return False

        print(html)
        soup = BeautifulSoup(html.text, "html.parser")
        childitem = soup.find_all(class_="market_listing_item_img_container")

        # 格式:{item_id: price}
        for i in range(len(childitem)):
            child: bs4.Tag = childitem[i]
            id = child.find(class_="market_listing_item_img")
            if id is None:
                return False
            else:
                return True

    while not gethtml():
        time.sleep(2)
        gethtml()

    print(html)

    if html.status_code != 200:
        print("失败")
    else:
        ass = assets.Assets(html.text)
        ass.setall()
        item_info = ass.itemdata

        sorted_item_info = sorted(item_info.items(), key=sortkey)  # float:磨损排序 priceandfee:价格排序
        restored_dict = OrderedDict(sorted_item_info)



        print(json.dumps(sorted_item_info, indent=4, sort_keys=True, ensure_ascii=False))



