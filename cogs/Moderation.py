import discord
from discord import app_commands
from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        pass

    # <<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>
    # clear Messages
    # <<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>
    @commands.hybrid_command(description="will delete a number of messages")
    @app_commands.describe(amount="the number of messages to delete")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = 5):
        await ctx.channel.purge(limit=amount+1)
        await ctx.send(f"I deleted {amount} messages for you", delete_after=5)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to do that")

    # --------------------------------------------------
    # Kick
    # --------------------------------------------------
    @commands.hybrid_command(description="will kick a member")
    @app_commands.describe(member="the member to kick")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f"{member.mention} has been kicked for {reason}")

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to do that")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please specify a member to kick")

    # <<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>
    # Ban
    # <<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>
    @commands.hybrid_command(description="will ban a member")
    @app_commands.describe(member="the member to ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f"{member.mention} has been banned for {reason}")
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to do that")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please specify a member to ban")

    # --------------------------------------------------
    # Un-Ban
    # --------------------------------------------------
    @commands.hybrid_command(description="will unban a member")
    @app_commands.describe(member="the member to unban")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"{user.mention} has been unbanned")
                return

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to do that")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please specify a member to unban")

    # <<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>
    # Mute
    # <<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>
    @commands.hybrid_command(description="will mute a member")
    @app_commands.describe(member="the member to mute")
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member):
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.add_roles(muted_role)
        await ctx.send(f"{member.mention} has been muted")

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to do that")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please specify a member to mute")

    # --------------------------------------------------
    # Un-Mute
    # --------------------------------------------------
    @commands.hybrid_command(description="will unmute a member")
    @app_commands.describe(member="the member to unmute")
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.remove_roles(muted_role)
        await ctx.send(f"{member.mention} has been unmuted")

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to do that")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please specify a member to unmute")


async def setup(bot):
    await bot.add_cog(Moderation(bot))
