from discord.ext import commands

from discord.ext.commands import has_guild_permissions

from utils.utils import Colors

from config.config import data

import discord


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'\n{Colors.Green}--> {Colors.Reset}Moderation commands ready')

    @commands.Cog.listener()
    async def on_message(self, message):
        message.content = str(message.content)

        msg = message.content.lower()
        msg = msg.split()

        if any(item in msg for item in data['BlackWords']):
            await message.delete()

            embed = discord.Embed(title='Black Word',
                                  description=f"Il bot ha segnalato allo staff l'utilizzo di una black word"
                                              f" da parte tua, digita {data['Prefix']}blackwords per avere"
                                              f" la lista delle black words del server",
                                  color=discord.Color.dark_purple())

            embed.add_field(name='Canale Server', value=str(message.channel.name), inline=False)
            embed.add_field(name='Autore Messaggio', value=str(message.author), inline=False)

            await message.author.send(embed=embed)

    @commands.command()
    @has_guild_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        try:
            if reason is None:
                await ctx.send(f'Impossibile espellere {member.mention}, devi specificare il motivo del kick!!')

            else:
                await ctx.guild.kick(member, reason=reason)
                await ctx.send(f"L'utente {member.mention} è stato espulso dal server per il seguente motivo: {reason}")

        except discord.HTTPException:
            embed = discord.Embed(title=f'Impossibile eseguire il comando {data["Prefix"]}kick',
                                  color=discord.Color.dark_purple())

            await ctx.channel.send(embed=embed)

    @commands.command()
    @has_guild_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        try:
            if reason is None:
                await ctx.send(f"Impossibile bannare {member.mention}, devi specificare il motivo del ban!!")

            else:
                if not member.bot:
                    await member.send(f'Sei stato bannato dal server per il seguente motivo: {reason}')

                await ctx.guild.ban(member, reason=reason)
                await ctx.channel.send(f"L'utente è stato bannato dal server da {ctx.author}")

        except discord.HTTPException:
            embed = discord.Embed(title=f'Impossibile eseguire il comando {data["Prefix"]}ban',
                                  color=discord.Color.dark_purple())

            await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Moderation(bot))
