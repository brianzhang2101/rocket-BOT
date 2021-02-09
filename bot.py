import os
import discord
import asyncio
from dotenv import load_dotenv
from subprocess import Popen
from hot import printHot

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()
loop = asyncio.get_event_loop()

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='the next rocket to Mars!'))
    print(f'{client.user} has connected to Discord!')
    Popen('python scan.py')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if '!hot' == message.content.lower():
        loop.create_task(printHot(message))
    elif '!search' in message.content.lower():
        await message.channel.send('In Progress!')
    elif '!price' in message.content.lower():
        await message.channel.send('In Progress!')
    elif '!help' == message.content.lower():
        embedVar = discord.Embed(title="How does this bot work?", description="""Comments data is scraped from subreddit [r/stocks](https://www.reddit.com/r/stocks/).
                                                    Data is analysed in order to find trending tickers that have an average gain of more or equal to 10% over the
                                                    last 3 days and the current comment count is more or equal to 15.""")
        embedVar.add_field(name="!hot", value="Returns a list of the hottest tickers of today.", inline=False)
        embedVar.add_field(name="[COMING SOON] !search <ticker>", value="Returns analysed ticker data. Data consists of the average % gain of the last 3 days and today's comment count.", inline=True)
        embedVar.add_field(name="[COMING SOON] !price <ticker>", value="Returns current price of <ticker>.", inline=False)
        embedVar.add_field(name="!version", value="Returns the current version of this bot. Patch notes are included.", inline=False)
        embedVar.add_field(name="!creator", value='\u200b', inline=False)
        await message.channel.send(embed=embedVar)
    elif '!version' == message.content.lower():
        embedVar = embedVar = discord.Embed(title="Version 1.0.0", description="Released 9th Feb 2021")
        embedVar.add_field(name="-> Rocket $BOT is officially public 🎉",value="-> Introducing !hot 🔥", inline=False)
        await message.channel.send(embed=embedVar)
    elif '!creator' == message.content.lower():
        embedVar = discord.Embed(title="Created by HeX#6292", description="Released 9th Feb 2021")
        await message.channel.send(embed=embedVar)
client.run(TOKEN)