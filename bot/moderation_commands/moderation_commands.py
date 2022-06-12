from discord.ext import commands
from discord.ext.commands import has_guild_permissions

from utils.enums import Colors

import discord


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'\n{Colors.Green}--> {Colors.Reset}Moderation commands ready')

    @commands.command()
    @has_guild_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if reason is None:
            await ctx.send(f'Impossibile espellere {member.mention}, devi specificare il motivo del kick!!')

        else:
            await ctx.guild.kick(member, reason=reason)
            await ctx.send(f"L'utente {member.mention} è stato espulso dal server per il seguente motivo: {reason}")

    @commands.command()
    @has_guild_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if reason is None:
            await ctx.send(f"Impossibile bannare {member.mention}, devi specificare il motivo del ban!!")

        else:
            await member.send(f'Sei stato bannato dal server per il seguente motivo: {reason}')
            await ctx.guild.ban(member, reason=reason)
            await ctx.channel.send(f"L'utente è stato bannato dal server da {ctx.author}")


def setup(bot):
    bot.add_cog(Moderation(bot))
