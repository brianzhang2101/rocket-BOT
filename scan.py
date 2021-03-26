import praw
import re
import requests
import json
import schedule
import time
import os 
from collections import defaultdict
from pymongo import MongoClient
from datetime import datetime, timedelta, date

# remove bad tickers - returns 1 if deleted or 0 if not deleted
def deleteData(collection, ticker):
    with open('badtickers.json') as json_file:
        data = json.load(json_file)
        if ticker in data["tickers"]:
            # TODO: maybe unless these tickers include a $
            collection.delete_one({"name":ticker})
            return(1)
    return(0)

# gets the collection - TODO: parameter should be dependent on what user needs like titles or comments
def getCollection():
    cluster = MongoClient("mongodb+srv://StocksBot:d7AIgwlYKTQRIWY0@cluster0.jwyf2.mongodb.net/StocksBot?retryWrites=true&w=majority")

    # TODO: Account for Title and Article Content in future!
    db = cluster["Tickers"]
    collection = db["Comments"]

    return collection

# add to MongoDB database
def addData(ticker, count):
    
    collection = getCollection()

    today = str(date.today())

    post = {"name": ticker, "score": count, "date": today}

    print("Added", ticker + "!")
    collection.insert_one(post)

# process title data TODO: Finish this function!
def get_titleData(toPrint):
    # read file lines
    top = open("top.txt", "r", encoding="utf-8")
    Lines = top.readlines()

    # initalise dictionary
    data = defaultdict(int)  

    # capture tickers from titles
    for line in Lines:
        content = line.partition("https://")
        for word in line.split():
            ticker = re.search("^\$*([A-Z]{1,5})$", word)
            if ticker:
                company = get_symbol(ticker.group(1))
                if company != ticker.group(1):
                    data[ticker.group(1)] += 1

    # print all tickers collected
    if print:      
        for key in sorted(data, key=data.get, reverse=True):
            if data[key] <= 1:
                print(key, "was ignored!")
            else:
                addData(key, data[key])

# process comments data
def get_commentsData(reddit):
    # read file lines
    top = open("top.txt", "r", encoding="utf-8")
    Lines = top.readlines()

    # initalise dictionary
    data = defaultdict(int)

    lineCount = 1

    # get post ID
    for line in Lines:
        # PRAW sometimes bugs out if post includes an IMGUR or similar link
        if (re.search("(?<=comments\/).*?(?=\/)", line)) is not None:
            ID = re.search("(?<=comments\/).*?(?=\/)", line).group()
            # scrape all comments
            submission = reddit.submission(id=ID)
            submission.comments.replace_more(limit=None)
            for comment in submission.comments.list():
                # get each word
                for word in comment.body.split():
                    ticker = re.search("^(\$)*([A-Z]{1,5})$", word)
                    # if ticker found
                    if ticker:
                        # verify the ticker is correct
                        company = get_symbol(ticker.group(2))
                        if company != ticker.group(2):
                            collection = getCollection()
                            # Allow bad tickers if it follows a $
                            badTicker = deleteData(collection, ticker.group(2))
                            if badTicker == 0:
                                data[ticker.group(2)] += 1
        
    # add tickers to database
    for key in sorted(data, key=data.get, reverse=True):
        if data[key] <= 1:
            print(key, "was ignored!")
        else:
            addData(key, data[key])
            collection = getCollection()
            deleteData(collection, key)

# get symbol - returns name of company if ticker exists TODO: please rename this function!
def get_symbol(symbol):
    url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(symbol)

    result = requests.get(url).json()

    for x in result['ResultSet']['Result']:
        if x['symbol'] == symbol:
            return x['name']
        else:
            return symbol

    return symbol

def main(): 
    # log into bot
    reddit = praw.Reddit(client_id='k3e93OiTMr6gpA', \
                        client_secret='-2rh0oZI4Zn5sZ8nNOM838rzdAux1Q', \
                        user_agent='TheStocksBot', \
                        username='TheStocksBot', \
                        password='Diamondhands42')

    # access r/stocks
    subreddit = reddit.subreddit("stocks")    

    # paste title and URL into file
    open("top.txt", "w").close()
    for i in subreddit.top(time_filter='day'):
        print(i.title, i.url, file=open("top.txt", "a", encoding="utf-8"))

    #get_titleData(0)

    print("Scraping comments data!", datetime.now())
    get_commentsData(reddit)
    print("Calculating gains!", datetime.now())
    os.system('python calculate.py')
    print("Analysing data!", datetime.now())
    os.system('python analyse.py')
      
# schedule the program 
if __name__=="__main__":
    schedule.every().day.at("04:00").do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)       