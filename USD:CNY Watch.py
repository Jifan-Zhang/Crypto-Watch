from Email import Email
import requests
from time import sleep
from datetime import datetime
import pytz
from random import randint

driver = Email()
driver.load_config("secrets.json")
while(True):
    try:
        payload = requests.get("http://api.coincap.io/v2/markets?baseSymbol=cny&quoteSymbol=usd",allow_redirects=True).content
    except:
        driver.send("USD/CNY Error", "Failed to get USD/CNY Payload.")
        break
    payload = eval(payload.decode('utf-8').replace("null","\"null\""))
    rate = round(1/float(payload["data"][0]["priceQuote"]), 4)
    if("last_rate" not in globals()):
        last_rate = rate

    if(round(rate%1) - round(last_rate%1)):
        time = datetime.fromtimestamp(2+payload["data"][0]["updated"]//1000).astimezone(pytz.timezone('US/Eastern'))\
                .strftime("%Y-%m-%d %H:%M:%S")
        msg = f"USD/CNY {'increased' if rate>last_rate else 'decreased'} from {last_rate} to {rate}.\n{time}"
        driver.send("USD/CNY Exchange Rate", msg)
        sleep(randint(10,30))
    last_rate = rate
