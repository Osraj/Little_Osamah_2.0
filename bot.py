# importing needed libraries
import discord
from discord.ext import commands
from discord import app_commands
from config import TOKEN # <-- This line is for the token

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
@bot.command(description="testing command")
async def ping(ctx):
    await ctx.send('Pong!')


# Running the bot
bot.run(TOKEN)
