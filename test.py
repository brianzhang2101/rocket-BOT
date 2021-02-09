import asyncio
import discord
from dotenv import load_dotenv
from subprocess import Popen
import os
from tester import sleep_and_add

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

loop = asyncio.get_event_loop()

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    loop.create_task(sleep_and_add(message))

client.run(TOKEN)