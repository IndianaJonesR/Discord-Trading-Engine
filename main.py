import discord
from discord.ext import commands
import asyncio

USER_TOKEN = "NjcyODM3MjIwOTUxOTE2NTQ1.Gny3oR.KMtODQXfiDWm7IY0WXa2BUrqdGKQh9yeNzC_oY"
TARGET_SERVER_ID = 990575817115463770  
TARGET_CHANNEL_ID = 990575817115463773

bot = commands.Bot(command_prefix="!", self_bot=True)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    
    #if message.author == bot.user:
        #return

    if message.guild and message.channel:
        if message.guild.id == TARGET_SERVER_ID and message.channel.id == TARGET_CHANNEL_ID:
            print(f"New message in {message.channel.name}:")
            print(f"Author: {message.author.name}")
            print(f"Content: {message.content}\n")

try:
    bot.run(USER_TOKEN)
except Exception as e:
    print(f"Error: {e}")