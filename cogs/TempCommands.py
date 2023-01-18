import discord
from discord import app_commands
from discord.ext import commands
import random
from datetime import datetime


class TempCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        pass

    # --------------------------------------------------
    # Embed
    # --------------------------------------------------
    async def embed(self, ctx, title, description, color):
        embed_message = discord.Embed(title=title, description=description, color=color, timestamp=datetime.now())
        embed_message.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar)
        embed_message.add_field(name="field1_name", value="field1_description", inline=False)
        embed_message.set_thumbnail(url=ctx.author.avatar)
        embed_message.set_image(url=ctx.guild.icon)
        embed_message.set_footer(text=f"ID: {ctx.author.id}")
        await ctx.send(embed=embed_message)
        return

    # <<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>
    # Mention Command
    # <<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>
    @commands.hybrid_command(description="will mention a user")
    @app_commands.describe(member="the member to mention", reason="the reason for the mention")
    async def mention(self, ctx, member: discord.Member, reason="No reason provided"):
        await self.embed(ctx, "Mention", f"<@{ctx.author.id}> mentioned {member.mention}", ctx.author.color)

    # --------------------------------------------------
    # Ping
    # --------------------------------------------------
    @commands.hybrid_command(description="Shows the bot's latency in ms.")
    async def ping(self, ctx):
        bot_latency = round(self.bot.latency * 1000)
        await ctx.send(f"Pong! \nbot latency: {bot_latency}ms")
        # await self.embed(ctx, "Ping", f"bot latency: {bot_latency}ms", 0x00ff00, "None")

    # <<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>
    # Add
    # <<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>
    @commands.hybrid_command(description="will add two numbers")
    @app_commands.describe(num1="the first number", num2="the second number")
    async def add(self, ctx, num1: int, num2: int):
        await ctx.send(num1 + num2)

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