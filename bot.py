# --------------------------------------------------
# importing needed libraries
# --------------------------------------------------
import asyncio
import json
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
# The Bot token will be imported from config.py


# <<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>
# The Bot configs
# <<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>
# Initializing the bot (not sure why we need this yet)
intents = discord.Intents.all()
intents.members = True
intents.message_content = True


# --------------------------------------------------
# Prefixes from prefixes.json file
# --------------------------------------------------
async def get_server_prefix(bot, message):
    with open("jsonfiles/prefixes.json", "r") as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

# --------------------------------------------------
# Initializing the bot
# --------------------------------------------------
bot = commands.Bot(command_prefix=get_server_prefix, description=bot_description, intents=discord.Intents.all())


# <<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>
# Adding prefixes to the prefixes.json file when the bot joins a server
# <<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>
@bot.event
async def on_guild_join(guild):
    with open("jsonfiles/prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = "!"

    with open("jsonfiles/prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)

# --------------------------------------------------
# Removing prefixes from the prefixes.json file when the bot leaves a server
# --------------------------------------------------
@bot.event
async def on_guild_remove(guild):
    with open("jsonfiles/prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open("jsonfiles/prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)


# <<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>
# Setting the bot prefix with a command
# <<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>
@bot.hybrid_command()
@commands.has_permissions(administrator=True)
async def set_prefix(ctx, new_prefix: str):
    with open("jsonfiles/prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = new_prefix

    with open("jsonfiles/prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)

    await ctx.send(f"Prefix set to {new_prefix}")

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
