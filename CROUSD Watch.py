from Email import Email
import requests
from time import sleep
from datetime import datetime
import pytz
from random import randint

driver = Email()
driver.load_config("secrets.json")
count = 0
while(True):
    try:
        payload = requests.get("https://api.nomics.com/v1/currencies/ticker?key=7d6f697fa23bbde3aa589fca5c6ec0600a442b65&ids=CRO&interval=1m&convert=USD&per-page=1&page=1").content
        payload = eval(payload.decode('utf-8').replace("null","\"null\""))
        rate = float(payload[0]['price'])
    
        if("last_rate" not in globals()):
            last_rate = rate

        if(round(last_rate*100)!=round(rate*100)):
            msg = f"CRO/USD {'increased' if rate>last_rate else 'decreased'} from {last_rate} to {rate}.\n"
            driver.send("CRO Exchange Rate", msg)
            break
        sleep(randint(8,12))
        last_rate = rate
        count+=1
    except:
        driver.send("CRO Error", f"Failed to get CRO Payload.\n{payload}\nAfter {count} iterations.")
        break
