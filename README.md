# rocket-$BOT
Discord bot that scrapes comments data from popular investment subreddits and analyses it to identify trending tickers 🚀

# How Does It Work?

Every day at 04:00 NY Time, the bot will run a script to scrape comments data from specific subreddits' top posts of the day.

Collated data is appended to a MongoDB database. Each ticker's mention count is compared to yesterday and this value is used for a 3-day rolling average calculation and returned as a percentage increase/decrease. For tickers that are regularly associated with common acronyms (e.g CEO is Chief Executive Officer, but $CEO is CNOOC Limited.) they are required to contain a prefix $, otherwise we can assume that it is a valid ticker.

If a ticker's current day mention count is below 15, it is not considered "hot". It also must have a 3-day rolling average of more than or equal to 10%.

# Known Issues

- There are currently message formatting issues for users on smaller screened devices such as mobile. This is a Discord embed message issue, will look into ASCII table alternatives.
- Unfortunately due to Heroku's use of ephemeral filesystem, the bot's current method of storing analysed ticker data is ineffective. Dynamic changes in text files like the one used here are only temporarily stored. This is because once every 24 hours, Heroku restarts all dynos and all on-day data is wiped. In order to fix this, I shall look into external methods of storage and deviate from using text files (most likely MongoDB).

# Coming Soon

- Looking at alternative finance APIs as the Yahoo one right now is only for querying for a company name and ticker. One that includes current prices will be idealistic. This is especially important for an upcoming feature: !price.
- !search - Look up stocks data for any ticker inside my database.
- Add more subreddits, particularly smaller ones (only supporting r/stocks right now). Problem is that bigger subreddits such as r/wallstreetbets may take much longer to fully scan all their comments since it is about 8 times bigger than r/stocks. Currently r/stocks takes about 15 minutes to fully scan and so there are concerns that the bot may crash/freeze up. 

# Note

Due to security concerns, you cannot post your API token online and so a .gitignore file was put in place my .env file. Please create your own bot/MongoDB database to run this.


