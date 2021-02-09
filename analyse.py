from pymongo import MongoClient
from datetime import datetime, timedelta, date

def main():
    cluster = MongoClient("mongodb+srv://StocksBot:d7AIgwlYKTQRIWY0@cluster0.jwyf2.mongodb.net/StocksBot?retryWrites=true&w=majority")

    db = cluster["Tickers"]
    collection = db["Comments"]

    findHotPicks(collection)

# Get average of last 3 days (including today)

def getAverage(ticker, collection):
    today = str(date.today())
    today_datetime = datetime.strptime(today, '%Y-%m-%d').date()
    total_gain = 0
    for n in range(0,3):
        daybefore_datetime = today_datetime - timedelta(days=n)
        # Day doesn't exist
        if len(list(collection.find({'name': ticker, 'date': daybefore_datetime.strftime("%Y-%m-%d")}))) == 0:
            continue
        else:
            for day in collection.find({'name': ticker, 'date': daybefore_datetime.strftime("%Y-%m-%d")}):
                total_gain += float(day["gain"])

    return total_gain / 3

def findHotPicks(collection):
    today = str(date.today())
    today_datetime = datetime.strptime(today, '%Y-%m-%d').date()
    outFile = open("out.txt", "w").close()
    print("The Hottest Stocks are:")
    for stock in collection.find({'date': today_datetime.strftime("%Y-%m-%d")}):
        ticker = stock["name"]
        average = round(getAverage(ticker, collection), 2)
        if stock["score"] < 15:
            break
        if average >= 10 and stock["score"] >= 15:
            print(ticker, str(average), str(stock["score"]), file=open("out.txt", "a"))
    outFile = open("out.txt", "a")
    outFile.write(datetime.now().strftime("%Y-%m-%d-%H:%M:%S"))

if __name__=="__main__":
    main()