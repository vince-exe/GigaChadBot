from discord.ext import commands

from discord.ext.commands import has_guild_permissions

from utils.utils import Colors

from config.config import data

import discord


class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'\n{Colors.Green}--> {Colors.Reset}Utilities commands ready')

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

    @commands.command()
    async def whois(self, ctx, member: discord.Member):
        embed = discord.Embed(title="Informazioni Utente",
                              color=discord.Color.dark_purple())

        role = str(member.top_role)
        if not role.startswith('@'):
            role = '@' + role

        fields = [("Nome", str(member), True),
                  ("ID", member.id, True),
                  ("Top Ruolo", role, False),
                  ("Data Creazione", member.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                  ("Entrato Nel Server", member.joined_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                  ]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        embed.set_thumbnail(url=member.avatar_url)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Utilities(bot))
