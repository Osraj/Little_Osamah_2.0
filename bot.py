# importing needed libraries
import discord
from discord.ext import commands, tasks
from discord import app_commands
from config import TOKEN  # <-- This line is for the token
import random
from itertools import cycle  # <-- This line is for the bot status cycle


# The Bot configs
bot_description = ''' a bot that does everything you want it to do '''
bot_prefix = "!"
# The Bot token will be imported from config.py


# Initializing the bot (not sure why we need this yet)
intents = discord.Intents.all()
intents.members = True
intents.message_content = True


# Initializing the bot
bot = commands.Bot(command_prefix= bot_prefix, description=bot_description, intents=discord.Intents.all())


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


@bot.hybrid_command(description="This command will be used to test the bot")
async def ping(ctx):
    bot_latency = round(bot.latency * 1000)
    await ctx.send(f"Pong! \nbot latency: {bot_latency}ms")


@bot.hybrid_command(description="Add 2 numbers together")
@app_commands.describe(num1 = "The first number", num2 = "The second number")
async def add(ctx, num1: int, num2: int):
    await ctx.send(num1 + num2)


@bot.hybrid_command(aliases= ["quote of the day", "quote"],description="will give you are random response")
async def random_quote(ctx):
    with open("Random_Quotes.txt", "r") as f:
        quotes = f.readlines()
        response = random.choice(quotes)
        await ctx.send(response)


# Running the bot
bot.run(TOKEN)
