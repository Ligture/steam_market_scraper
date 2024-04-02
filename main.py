import steamscraper
import threading
url = 'https://steamcommunity.com/market/listings/730/MP5-SD%20%7C%20Liquidation%20%28Field-Tested%29'
query = {"start": 0, "count": 100}
steamscraper.scrape(url, query)