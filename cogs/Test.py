from discord.ext import commands

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(description="for testing the bot")
    async def test(self, ctx):
        await ctx.send("testing")


async def setup(bot):
    await bot.add_cog(Test(bot))