import asyncio
import discord
import os

async def sleep_and_add(message):
    await asyncio.sleep(3)
    await message.channel.send(message.channel.id)