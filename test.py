from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://StocksBot:d7AIgwlYKTQRIWY0@cluster0.jwyf2.mongodb.net/StocksBot?retryWrites=true&w=majority")

# TODO: Account for Title and Article Content in future!
db = cluster["Tickers"]
collection = db["Comments"]

myquery = { "date": "2021-02-10" }

collection.delete_many(myquery)