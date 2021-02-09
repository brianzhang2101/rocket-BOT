from datetime import datetime, timedelta, date
import os
import discord
import asyncio
import re

async def printHot(message):
    await asyncio.sleep(1)
    embedVar = discord.Embed(title="Ticker:                   Average Gain:         Today's Count:", colour=0x02de23)
    time_file = open("out.txt", "r")
    Lines = time_file.readlines()
    prev_line = None
    lineCount = 0
    for line in Lines:
        if prev_line is not None:
            find = re.search("([A-Z]*) (.*?) ([0-9]*)", prev_line)
            embedVar.add_field(name="\u200b", value=find.group(1), inline=True)
            percentage = str(find.group(2)) + "%"
            embedVar.add_field(name="\u200b", value=percentage, inline=True)
            embedVar.add_field(name="\u200b", value=find.group(3), inline=True)
        prev_line = line
        lineCount += 1
    timeFin = datetime.strptime(line, '%Y-%m-%d-%H:%M:%S')
    timeAgo = datetime.now() - timeFin
    timeUpdate = "Updated " + str(timeAgo.seconds//3600) + " hours and " + str((timeAgo.seconds//60)%60) + " minutes ago 🚀"
    embedVar.set_footer(text=timeUpdate)
    if lineCount == 1:
        fullMessage = "No tickers are hot right now :frowning2:\n" + timeUpdate
        await message.channel.send(fullMessage)
    else:
        await message.channel.send(embed=embedVar)
    time_file.close()

