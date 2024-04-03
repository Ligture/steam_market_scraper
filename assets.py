import bs4
import requests
from bs4 import BeautifulSoup
import json

g_rgAssets = ""
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "accept-language": "zh-cn"
}

class Assets:
    def __init__(self, html):
        self.g_rgAssets = ""
        self.g_rgListingInfo = ""
        self.html = html
        self.all_inspectlinks = []
        self.initial()
        self.itemdata = {

        }
        self.list = {}
        self.asset = {}
        self.initial()
    def initial(self):
        soup = BeautifulSoup(self.html, "html.parser")
        a = soup.find_all("script")
        g_rgAssets1 = ""
        for i in a:
            if "g_rgAssets" in i.text:
                start = i.text.find("g_rgAssets")
                end = i.text.find("g_rgCurrency")
                g_rgAssets1 = i.text[start + 13: end - 4].strip().strip(";")
                break
        self.g_rgAssets = g_rgAssets1

        g_rglistinginfo1 = ""
        for i in a:
            if "g_rgListingInfo" in i.text:
                start = i.text.find("g_rgListingInfo")
                end = i.text.find("g_plotPriceHistory")
                g_rglistinginfo1 = i.text[start + 17: end - 4].strip().strip(";")
                break
        self.g_rgListingInfo = g_rglistinginfo1

        #print(self.g_rgAssets)
        #print(self.g_rgListingInfo)
        self.asset = json.loads(self.g_rgAssets)
        self.list = json.loads(self.g_rgListingInfo)

    def setitemdata(self,itemid):
        assetid = self.list[itemid]['asset']['id']
        link = self.list[itemid]['asset']['market_actions'][0]['link']
        link = link.replace("%assetid%", assetid).replace("%listingid%", itemid)
        self.itemdata[itemid] = {}
        self.itemdata[itemid]['assetid'] = assetid
        self.itemdata[itemid]['inspectlink'] = link

        self.itemdata[itemid]['marketname'] = self.asset['730']['2'][assetid]['market_name']
        self.itemdata[itemid]['priceandfee'] = self.list[itemid]['price']+self.list[itemid]['fee']


    def setall(self):
        for i in self.list:
            self.setitemdata(i)
        #self.price()
        for i in self.itemdata:
            self.getfloat(self.itemdata[i]['inspectlink'])

    def price(self):
        soup = BeautifulSoup(self.html, "html.parser")
        childitem = soup.find_all(class_="market_listing_item_img_container")

        # 格式:{item_id: price}
        for i in range(len(childitem)):
            child: bs4.Tag = childitem[i]
            id = child.find(class_="market_listing_item_img")
            id1 = id.get("id")
            if id1[0:7] == "listing":
                item_id = id1[0:-6]
                price = child.parent.find(
                        class_="market_listing_right_cell market_listing_their_price"
                    ).find("span", class_="market_listing_price_with_fee")
                price = price.getText(strip=True)
                self.itemdata[item_id[8:]]['price'] = price
                self.itemdata[item_id[8:]]['pricenum'] = float(''.join(filter(lambda x: x.isdigit() or x == '.', price))) #提取数字价格方便排序

    def getfloat(self, inslink):
        data = requests.get(f"http://127.0.0.1:8010/?url={inslink}", verify=False, timeout=3, headers=headers)
        data = json.loads(data.text)
        float = data["iteminfo"]["floatvalue"]
        paintseed = data["iteminfo"]["paintseed"]
        itemid = data["iteminfo"]["m"]
        self.itemdata[itemid]['float'] = float
        self.itemdata[itemid]['paintseed'] = paintseed
