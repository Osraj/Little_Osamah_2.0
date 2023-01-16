# importing needed libraries
import discord
from discord.ext import commands
from discord import app_commands
from config import TOKEN # <-- This line is for the token
import random

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
    print(f'Logged in as [{bot.user}] (ID: {bot.user.id})')
    print('------')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} commands')
    except Exception as e:
        print(f'Failed to sync commands: {e}')


# a Testing Command
@bot.hybrid_command(description="This command will be used to test the bot")
async def ping(ctx):
    await ctx.send('Pong!')


@bot.hybrid_command(description="Add 2 numbers together")
@app_commands.describe(num1 = "The first number", num2 = "The second number")
async def add(ctx, num1: int, num2: int):
    await ctx.send(num1 + num2)


@bot.hybrid_command(description="will give you are random response")
async def random_quote(ctx):
    with open("Random_Quotes.txt", "r") as f:
        quotes = f.readlines()
        response = random.choice(quotes)
        await ctx.send(response)



# Running the bot
bot.run(TOKEN)
