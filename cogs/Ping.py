from discord.ext import commands


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Ping.py is ready")

    # --------------------------------------------------
    # The Actual Command Code
    # --------------------------------------------------
    @commands.hybrid_command(description="Shows the bot's latency in ms.")
    async def ping(self, ctx):
        bot_latency = round(self.bot.latency * 1000)
        await ctx.send(f"Pong! \nbot latency: {bot_latency}ms")


# --------------------------------------------------
# connecting this file to the main one
# --------------------------------------------------
async def setup(bot):
    await bot.add_cog(Ping(bot))
