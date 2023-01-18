import discord
from discord import app_commands, Color
from discord.ext import commands
from datetime import datetime


class ModCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        pass

    # <<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>
    # config
    # <<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>
    kick_color = discord.Color.yellow()
    ban_color = discord.Color.red()
    unban_color = discord.Color.green()
    mute_color = discord.Color.blue()
    unmute_color = discord.Color.green()

    # --------------------------------------------------
    # Embed
    # --------------------------------------------------
    async def embed_for_mods(self, ctx, title, description, color, reason=None):
        embed_message = discord.Embed(title=title, description=description, color=color, timestamp=datetime.now())
        embed_message.set_author(name=f"Requested by {ctx.author}", icon_url=ctx.author.avatar)
        embed_message.set_thumbnail(url=ctx.author.avatar)
        embed_message.add_field(name="Reason", value=reason, inline=False)
        embed_message.set_footer(text=f"ID: {ctx.author.id}")
        await ctx.send(embed=embed_message)
        return

    # <<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>
    # clear Messages
    # <<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>
    @commands.hybrid_command(description="will delete a number of messages")
    @app_commands.describe(amount="the number of messages to delete")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = 1):
        await ctx.channel.purge(limit=amount+1)
        await ctx.send(f"I deleted {amount} messages for you", delete_after=5)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to do that")
        if isinstance(error, commands.BadArgument):
            await ctx.send("Please enter a valid number")
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("I don't have permission to do that")

    # --------------------------------------------------
    # Kick
    # --------------------------------------------------
    @commands.hybrid_command(description="will kick a member")
    @app_commands.describe(member="the member to kick")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, reason="No reason provided"):
        await member.kick(reason=reason)
        # await self.embed_for_mods(ctx, "Kick Member", f"<@{ctx.author.id}> kicked <@{member.id}>", self.kick_color, reason)
        await ctx.send(f"<@{member.id}> was kicked by <@{ctx.author.id}> for {reason}", delete_after=10)
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to do that")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please specify a member to kick")
        if isinstance(error, commands.BadArgument):
            await ctx.send("Please enter a valid member to kick")
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("I can't kick that member")

    # <<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>
    # Ban
    # <<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>
    @commands.hybrid_command(description="will ban a member")
    @app_commands.describe(member="the member to ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        # await self.embed_for_mods(ctx, "Ban Member", f"<@{ctx.author.id}> Banned <@{member.id}>", self.ban_color, reason)
        await ctx.send(f"<@{member.id}> was banned by <@{ctx.author.id}> for {reason}", delete_after=10)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to do that")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please specify a member to ban")
        if isinstance(error, commands.BadArgument):
            await ctx.send("Please enter a valid member to ban")
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("I can't ban that member")

    # --------------------------------------------------
    # Un-Ban
    # --------------------------------------------------
    @commands.hybrid_command(description="will unban a member")
    @app_commands.describe(member="the member to unban")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member: discord.Member, reason=None):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                # await self.embed_for_mods(ctx, "Unban Member", f"<@{ctx.author.id}> Unbanned <@{member.id}>", self.unban_color, reason)
                await ctx.send(f"<@{member.id}> was unbanned by <@{ctx.author.id}> for {reason}", delete_after=10)
                return

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to do that")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please specify a member to unban")
        if isinstance(error, commands.BadArgument):
            await ctx.send("Please enter a valid member to unban")
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("I can't unban that member, or that member is not banned")

    # <<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>
    # Mute
    # <<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>
    @commands.hybrid_command(description="will mute a member")
    @app_commands.describe(member="the member to mute")
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, reason):
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.add_roles(muted_role)
        # await self.embed_for_mods(ctx, "Mute Member", f"<@{ctx.author.id}> Muted <@{member.id}>", self.mute_color, reason)
        await ctx.send(f"<@{member.id}> was muted by <@{ctx.author.id}> for {reason}", delete_after=10)

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to do that")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please specify a member to mute")
        if isinstance(error, commands.BadArgument):
            await ctx.send("Please enter a valid member to mute")
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("I can't mute that member, or that member is already muted")

    # --------------------------------------------------
    # Un-Mute
    # --------------------------------------------------
    @commands.hybrid_command(description="will unmute a member")
    @app_commands.describe(member="the member to unmute")
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member, reason):
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.remove_roles(muted_role)
        # await self.embed_for_mods(ctx, "Unmute Member", f"<@{ctx.author.id}> unmuted <@{member.id}>", self.unmute_color, reason)
        await ctx.send(f"<@{member.id}> was unmuted by <@{ctx.author.id}> for {reason}", delete_after=10)

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to do that")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please specify a member to unmute")
        if isinstance(error, commands.BadArgument):
            await ctx.send("Please enter a valid member to unmute")
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("I can't unmute that member, or that member is not muted")


async def setup(bot):
    await bot.add_cog(ModCommands(bot))
