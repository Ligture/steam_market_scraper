import bs4
import requests
from bs4 import BeautifulSoup
import inspectlink
import json


proxy = {
    #'http': 'socks5://127.0.0.1:7890',
    #'https': 'socks5://127.0.0.1:7890'
    # "http": "http://10.10.1.10:3128",
    # "https": "http://10.10.1.10:1080",
}


def parser(html):
    soup = BeautifulSoup(html, "html.parser")
    childitem = soup.find_all(class_="market_listing_item_img_container")

    # 格式:{item_id: price}

    items = {}
    for i in range(len(childitem)):
        child: bs4.Tag = childitem[i]
        id = child.find(class_="market_listing_item_img")

        id1 = id.get("id")
        try:
            if id1[0:7] == "listing":
                item_id = id1[0:-6]
                price = child.parent.find(
                    class_="market_listing_right_cell market_listing_their_price"
                ).find("span", class_="market_listing_price_with_fee")
                price = price.getText(strip=True)

                items[item_id] = price
        except BaseException as e:
            print(e)
    print(items)
    return items


def getfloat(inslink, price, unit="CNY"):
    currency = {
        "₴": "UAH",
        "¥": "CNY",
        "₸": "KZT",
        "₪": "ILS",
        "$": "USD",
        "zł": "PLN",
        "NT$": "TWD",
        "₩": "KRW",
        "pуб.": "RUB",
        "CHF": "CHF",
        'kr': 'SEK',
        'A$': 'AUD',
        'R$': 'BRL',
        '₫': 'VND'
    }
    data = requests.get(f"http://127.0.0.1/?url={inslink}")
    data = json.loads(data.text)
    print(data)
    float = data["iteminfo"]["floatvalue"]
    paintseed = data["iteminfo"]["paintseed"]
    assetid = data["iteminfo"]["a"]
    itemid = data["iteminfo"]["m"]
    return assetid, float, paintseed, price["listing_" + itemid]


query = {"start": 0, "count": 100}  # 不知道作用  # 10 25 50 100
checkurl = "https://steamcommunity.com/market/listings/730/MP5-SD%20%7C%20Liquidation%20%28Field-Tested%29"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "accept-language": "zh-cn",
}
html = requests.get(checkurl, headers=headers, proxies=proxy, params=query)
if html.status_code != 200:
    print("失败")
else:
    item_info = []

    # {item_id:price}
    items = parser(html.text)
    ins = inspectlink.Assets(html.text)
    links = ins.getallinspectlinks()
    for i in links:
        item_info.append(getfloat(i, items))

    item_info.sort(key=lambda x: x[1])
    print(item_info)
