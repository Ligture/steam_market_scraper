from bs4 import BeautifulSoup
import json

g_rgAssets = ""


class Assets:
    def __init__(self, html):
        self.g_rgAssets = ""
        self.html = html
        self.all_inspectlinks = []
        self.initial()

    def initial(self):
        soup = BeautifulSoup(self.html, "html.parser")
        a = soup.find_all("script")
        g_rgAssets1 = ""
        for i in a:
            if "g_rgAssets" in i.text:
                start = i.text.find("g_rgAssets")
                end = i.text.find("g_rgCurrency")
                g_rgAssets1 = i.text[start + 13 : end - 4].strip().strip(";")
        self.g_rgAssets = g_rgAssets1
        print(self.g_rgAssets)
        j = json.loads(self.g_rgAssets)
        print(j)
        self.all_inspectlinks = []
        for i in j["730"]["2"]:
            print(i)
            self.all_inspectlinks.append((i, j["730"]["2"][i]["actions"][0]["link"]))
        print(self.all_inspectlinks)

    def getinspectlinkbyid(self, id):
        for i in self.all_inspectlinks:
            if i[1].find(id) != -1:
                assetid = i[0]
                url = i[1].replace("%assetid%", assetid)
                return url
            else:
                return None

    def getallinspectlinks(self):
        links = []
        for i in self.all_inspectlinks:
            assetid = i[0]
            url = i[1].replace("%assetid%", assetid)
            links.append(url)
        return links
