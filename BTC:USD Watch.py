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
        payload = requests.get("https://api.coincap.io/v2/rates/bitcoin",allow_redirects=True).content
    except:
        driver.send("BTC Error", "Failed to get BTC Payload.")
        break
    payload = eval(payload.decode('utf-8').replace("null","\"null\""))
    rate = round(float(payload["data"]['rateUsd']))
    if("last_rate" not in globals()):
        last_rate = rate

    for _num in range(last_rate, rate+1):
        if(_num%500==0):
            msg = f"USD/CNY {'increased' if rate>last_rate else 'decreased'} from {last_rate} to {rate}.\n"
            driver.send("BTC Exchange Rate", msg)
            sleep(randint(8,12))
            break
    last_rate = rate
