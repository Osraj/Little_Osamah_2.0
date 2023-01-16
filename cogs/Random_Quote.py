from discord.ext import commands
import random


class Random_Quote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Random_Quote.py is ready")

    # --------------------------------------------------
    # The Actual Command Code
    # --------------------------------------------------
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
    await bot.add_cog(Random_Quote(bot))
