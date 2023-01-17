import discord
from discord import app_commands
from discord.ext import commands
import random


class TempCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        pass

    # --------------------------------------------------
    # Ping
    # --------------------------------------------------
    @commands.hybrid_command(description="Shows the bot's latency in ms.")
    async def ping(self, ctx):
        bot_latency = round(self.bot.latency * 1000)
        await ctx.send(f"Pong! \nbot latency: {bot_latency}ms")

    # <<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>
    # Add
    # <<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>
    @commands.hybrid_command(description="will add two numbers")
    @app_commands.describe(num1="the first number", num2="the second number")
    async def add(self, ctx, num1: int, num2: int):
        await ctx.send(num1 + num2)

    # --------------------------------------------------
    # Embed
    # --------------------------------------------------
    @commands.hybrid_command(description="will send an embed")
    async def embed(self, ctx):
        embed_message = discord.Embed(title="Embed Title", description="Embed Description", color=ctx.author.color)
        embed_message.set_author(name=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar)
        embed_message.add_field(name="Field 1", value="Field 1 Value", inline=False)
        embed_message.add_field(name="Field 2", value="Field 2 Value", inline=False)
        embed_message.add_field(name="Field 3", value="Field 3 Value", inline=False)
        embed_message.set_thumbnail(url=ctx.guild.icon)
        embed_message.set_image(url=ctx.guild.icon)
        embed_message.set_footer(text="Embed Footer", icon_url=ctx.author.avatar)

        await ctx.send(embed=embed_message)

    # <<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>
    # Random_Quote
    # <<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>
    @commands.hybrid_command(aliases=["quote of the day", "quote"], description="will give you are random response")
    async def random_quote(self, ctx):
        with open("Random_Quotes.txt", "r") as f:
            quotes = f.readlines()
            response = random.choice(quotes)
            await ctx.send(response)

# --------------------------------------------------
# connecting this file to the main one
# --------------------------------------------------
async def setup(bot):
    await bot.add_cog(TempCommands(bot))