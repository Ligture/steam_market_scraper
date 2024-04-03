import steamscraper
import threading
import time
url = [
       'https://steamcommunity.com/market/listings/730/MAG-7%20%7C%20Insomnia%20%28Field-Tested%29',
       'https://steamcommunity.com/market/listings/730/SCAR-20%20%7C%20Fragments%20%28Field-Tested%29',
       'https://steamcommunity.com/market/listings/730/Tec-9%20%7C%20Rebel%20%28Field-Tested%29',
       'https://steamcommunity.com/market/listings/730/R8%20Revolver%20%7C%20Banana%20Cannon%20%28Field-Tested%29',
    'https://steamcommunity.com/market/listings/730/Dual%20Berettas%20%7C%20Flora%20Carnivora%20%28Field-Tested%29'



       ]
query = {"start": 0, "count": 5}
def run_thread(args,waittime):
    while True:
        thread = threading.Thread(target=steamscraper.scrape, args=args)
        thread.start()
        thread.join()
        time.sleep(waittime)


for i in url:
    th1 = threading.Thread(target=run_thread, args=((i, query, lambda x: x[1]['float'], 0.21),15))
    th1.start()
