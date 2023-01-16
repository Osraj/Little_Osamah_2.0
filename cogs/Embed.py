import discord
from discord import app_commands
from discord.ext import commands


class Embed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        # print("Embed.py is ready")
        pass

    # --------------------------------------------------
    # The Actual Command Code
    # --------------------------------------------------
    @commands.hybrid_command(description="will send an embed")
    async def embed(self, ctx):
        embed_mesasge = discord.Embed(title="Embed Title", description="Embed Description", color=ctx.author.color)
        embed_mesasge.set_author(name=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar)
        embed_mesasge.add_field(name="Field 1", value="Field 1 Value", inline=False)
        embed_mesasge.add_field(name="Field 2", value="Field 2 Value", inline=False)
        embed_mesasge.add_field(name="Field 3", value="Field 3 Value", inline=False)
        embed_mesasge.set_thumbnail(url=ctx.guild.icon)
        embed_mesasge.set_image(url=ctx.guild.icon)
        embed_mesasge.set_footer(text="Embed Footer", icon_url=ctx.author.avatar)

        await ctx.send(embed=embed_mesasge)


async def setup(bot):
    await bot.add_cog(Embed(bot))