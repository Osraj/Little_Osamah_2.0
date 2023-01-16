# importing needed libraries
import asyncio
import os
import discord
from discord.ext import commands, tasks
from config import TOKEN  # <-- This line is for the token
from itertools import cycle  # <-- This line is for the bot status cycle

# Enabling logging for this bot
discord.utils.setup_logging()

# The Bot configs
bot_description = ''' a bot that does everything you want it to do '''
bot_prefix = "!"
# The Bot token will be imported from config.py


# Initializing the bot (not sure why we need this yet)
intents = discord.Intents.all()
intents.members = True
intents.message_content = True


# Initializing the bot
bot = commands.Bot(command_prefix=bot_prefix, description=bot_description, intents=discord.Intents.all())


# The bot is ready message + how many commands are loaded
@bot.event
async def on_ready():
    change_status.start()
    await bot.change_presence(status=discord.Status.online)
    print(f'Logged in as [{bot.user}] (ID: {bot.user.id})')
    print('------')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} commands')
    except Exception as e:
        print(f'Failed to sync commands: {e}')


# The bot status cycle
bot_activity, bot_status = \
    cycle([discord.ActivityType.watching, discord.ActivityType.listening, discord.ActivityType.watching]), \
    cycle(["After all of you", "all of your needs", "you having fun ^^"])


@tasks.loop(seconds=20)
async def change_status():
    await bot.change_presence(activity=discord.Activity(type=next(bot_activity), name=next(bot_status)))


# loading cogs
async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"{filename[:-3]} is Loaded")


async def main():
    async with bot:
        await load()
        await bot.start(TOKEN)


# Running the bot
asyncio.run(main())
