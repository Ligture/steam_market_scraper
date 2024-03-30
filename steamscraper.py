import bs4
import requests
from bs4 import BeautifulSoup
import inspectlink
import json


proxy = {
    #'http': 'socks5://127.0.0.1:7890',
    #'https': 'socks5://127.0.0.1:7890'
    #"http": "http://10.10.1.10:3128",
    #"https": "http://10.10.1.10:1080",

}
def parser(html):
    soup = BeautifulSoup(html, 'html.parser')
    childitem = soup.find_all(class_='market_listing_item_img_container')
    item_ids = []
    for i in range(len(childitem)):
        child: bs4.Tag = childitem[i]
        id = child.find(class_='market_listing_item_img')
        id1 = id.get('id')
        try:
            if id1[0:7] == 'listing':
                item_id = id1[0:-6]
                item_ids.append(item_id)
        except BaseException as e:
            print(e)
    print(item_ids)
    return item_ids

def getfloat(inslink):
    data = requests.get(f'http://127.0.0.1/?url={inslink}')
    data = json.loads(data.text)
    print(data)
    float = data['iteminfo']['floatvalue']
    paintseed = data['iteminfo']['paintseed']
    assetid = data['iteminfo']['a']
    return assetid, float, paintseed


checkurl = 'https://steamcommunity.com/market/listings/730/MP5-SD%20%7C%20Liquidation%20%28Field-Tested%29'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'}
html = requests.get(checkurl,
                    headers=headers,
                    proxies=proxy)
if html.status_code != 200:
    print('失败')
else:
    item_info = []
    item_ids = parser(html.text)
    ins = inspectlink.Assets(html.text)
    links = ins.getallinspectlinks()
    for i in links:
        item_info.append(getfloat(i))
    item_info.sort(key=lambda x:x[1])
    print(item_info)





