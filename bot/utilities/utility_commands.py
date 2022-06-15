from discord.ext import commands

from discord.ext.commands import has_guild_permissions

from utils.utils import Colors

from config.config import data

from bot.utilities.utility_utils import *

import discord


class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'\n{Colors.Green}--> {Colors.Reset}Utilities commands ready')

    # clear the chat based on the given number of message to clear
    @commands.command()
    @has_guild_permissions(manage_channels=True)
    async def clear_(self, ctx, limit_=None):
        if limit_ is None:
            await ctx.send(f'Parametri insufficienti, digita {data["Prefix"]}help per maggiori informazioni')

        else:
            await ctx.channel.purge(limit=int(limit_))

    # Clear the All the chat
    @commands.command()
    @has_guild_permissions(manage_channels=True)
    async def clear(self, ctx):
        await ctx.channel.purge()

    # return the info about a user
    @commands.command()
    async def whois(self, ctx, member: discord.Member):
        role = str(member.top_role)
        if not role.startswith('@'):
            role = '@' + role

        await ctx.send(embed=get_whois_embed(member, role))

    # take the id of a channel and return the channel name
    @commands.command()
    @has_guild_permissions(manage_channels=True)
    async def chinfo(self, ctx, *, channel_id=None):
        if channel_id is not None:
            channel = ctx.guild.get_channel(int(channel_id))
            if channel is not None:
                await ctx.channel.send(embed=get_channel_info_embed(ctx, channel))


def setup(bot):
    bot.add_cog(Utilities(bot))
