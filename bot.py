# --------------------------------------------------
# importing needed libraries
# --------------------------------------------------
import asyncio
import os
import discord
from discord import app_commands
from discord.ext import commands, tasks
from config import TOKEN  # <-- This line is for the token
from itertools import cycle  # <-- This line is for the bot status cycle

# <<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>
# Enabling logging for this bot
# <<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>
discord.utils.setup_logging()

# --------------------------------------------------
# The Bot configs
# --------------------------------------------------
bot_description = ''' a bot that does everything you want it to do '''
bot_prefix = "!"
# The Bot token will be imported from config.py


# <<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>
# The Bot configs
# <<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>
# Initializing the bot (not sure why we need this yet)
intents = discord.Intents.all()
intents.members = True
intents.message_content = True


# --------------------------------------------------
# Initializing the bot
# --------------------------------------------------
bot = commands.Bot(command_prefix=bot_prefix, description=bot_description, intents=discord.Intents.all())


# <<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>
# The bot is ready message + how many commands are loaded
# <<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>
@bot.event
async def on_ready():
    change_status.start()
    await bot.change_presence(status=discord.Status.online)
    print('------')
    print(f'Logged in as [{bot.user}] (ID: {bot.user.id})')
    print('------')
    try:
        synced = await bot.tree.sync()
        # print(f'Synced {len(synced)} commands')
    except Exception as e:
        print(f'Failed to sync commands: {e}')


# --------------------------------------------------
# The bot status cycle
# --------------------------------------------------
bot_activity, bot_status = \
    cycle([discord.ActivityType.watching, discord.ActivityType.listening, discord.ActivityType.watching]), \
    cycle(["After all of you", "all of your needs", "you having fun ^^"])


@tasks.loop(seconds=20)
async def change_status():
    await bot.change_presence(activity=discord.Activity(type=next(bot_activity), name=next(bot_status)))


# <<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>
# loading cogs
# <<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>
async def load():
    synced_cogs = []
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            synced_cogs.append(filename[:-3])
    print("----------------------------------------")
    print(f"Loaded Cogs: {synced_cogs}")
    cogs_count = len(synced_cogs)
    print(f"Synced Files: {cogs_count}")
    print("----------------------------------------")


async def unload():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.unload_extension(f"cogs.{filename[:-3]}")


@bot.hybrid_command(description="for reloading cogs")
@app_commands.describe(cog="The cog to reload")
async def reload(ctx, cog="all cogs"):
    await unload()
    await load()
    await ctx.send(f"Reloaded {cog}")


# --------------------------------------------------
# Running the bot
# --------------------------------------------------
async def main():
    async with bot:
        await load()
        await bot.start(TOKEN)
asyncio.run(main())
