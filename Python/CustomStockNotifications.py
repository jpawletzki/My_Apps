#This program checks if the time is during market hours and if it is, it will read tickers.txt which contains various stock tickers to reach out to for quotes.
#It gets run through the AlphaVantage API and is returned as a JSON object. The objects are appended to the email message and sent out over SMTP to the specified account.
#Code will not run as information is obfuscated


import requests
import json
import time
import smtplib
from datetime import datetime
from pytz import timezone
import re
StockTickers = []
TickerResults = []
EmailMessage = ""
TimeRe = re.compile("(9:..:..|10:..:..|11:..:..|12:..:..|13:..:..|14:..:..|15:..:..|16:..:..)")
est = timezone("US/Eastern")
if TimeRe.findall(str(datetime.now(est))):
    with open("Tickers.txt") as TickersFile:
        OpenTickerFile = TickersFile.readlines()
        for Ticker in OpenTickerFile:
            StockTickers.append(Ticker.strip())

    for Ticker in StockTickers:
        StockRequest = requests.get(f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={Ticker}&apikey=")
        JSONStockResponse = json.loads(StockRequest.text)
        TickerResults.append((json.dumps(JSONStockResponse, sort_keys=True, indent=4)))
        time.sleep(12)

    for Ticker in TickerResults:
        EmailMessage = EmailMessage + Ticker + "\n\n"

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login("", "")
        email_text = f"Subject: Stock Price Update\n \n{EmailMessage}"
        server.sendmail("", "", email_text)
    except:
        print('Error with Gmail Connection')


