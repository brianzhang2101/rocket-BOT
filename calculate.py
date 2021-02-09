from pymongo import MongoClient
from datetime import datetime, timedelta, date

cluster = MongoClient("mongodb+srv://StocksBot:d7AIgwlYKTQRIWY0@cluster0.jwyf2.mongodb.net/StocksBot?retryWrites=true&w=majority")

db = cluster["Tickers"]
collection = db["Comments"]

today = str(date.today())

today_datetime = datetime.strptime(today, '%Y-%m-%d').date()

today_score = 0
yesterday_score = 0

yesterday_datetime = today_datetime - timedelta(days=1)

# if today is day 0
if len(list(collection.find({'date': yesterday_datetime.strftime("%Y-%m-%d")}))) == 0:
    for instance in collection.find({'date': today_datetime.strftime("%Y-%m-%d")}):
        ticker = instance["name"]
        collection.update_one({'name': ticker, 'date': today_datetime.strftime("%Y-%m-%d")},{"$set": {"gain": 0}})
else:
    for today in collection.find({'date': today_datetime.strftime("%Y-%m-%d")}):
        today_score = 0
        ticker = today["name"]
        yesterday_datetime = today_datetime - timedelta(days=1)
        today_score = today["score"]
        # ticker doesn't exist yesterday
        if collection.count_documents({'name': ticker, 'date': yesterday_datetime.strftime("%Y-%m-%d")}) <= 0:
            ratio = 100
            collection.update_one({'name': ticker, 'date': today_datetime.strftime("%Y-%m-%d")},{"$set": {"gain": ratio}})
        else:
            # only runs if yesterday exists (will not run day 0 of script running officially)
            for instance in collection.find({'name': ticker, 'date': yesterday_datetime.strftime("%Y-%m-%d")}):
                yesterday_score = instance["score"]
                # yesterday, the ticker was never mentioned, but today it has more than 1
                if yesterday_score == 0:
                    ratio = 100
                else:
                    ratio = ((today_score - yesterday_score) / yesterday_score) * 100
                collection.update_one({'name': ticker, 'date': today_datetime.strftime("%Y-%m-%d")},{"$set": {"gain": ratio}})
