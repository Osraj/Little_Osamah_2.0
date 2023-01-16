from discord import app_commands
from discord.ext import commands


class Add(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Add.py is ready")

    # --------------------------------------------------
    # The Actual Command Code
    # --------------------------------------------------
    @commands.hybrid_command(description="will add two numbers")
    @app_commands.describe(num1="the first number", num2="the second number")
    async def add(self, ctx, num1: int, num2: int):
        await ctx.send(num1 + num2)


# --------------------------------------------------
# connecting this file to the main one
# --------------------------------------------------
async def setup(bot):
    await bot.add_cog(Add(bot))
