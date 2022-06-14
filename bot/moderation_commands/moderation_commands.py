from discord.ext import commands

from discord.ext.commands import has_guild_permissions

from utils.utils import Colors

from config.config import data

from utils.utils import get_date

import discord


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_channel_id = int(data['LogChannel'])

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
                                  description=f"I l bot ha segnalato allo staff l'utilizzo di una black word"
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
            if reason is not None:
                if not member.bot:
                    embed = discord.Embed(title='Messaggio dal Server',
                                          description='sei stato espulso dal server',
                                          color=discord.Color.dark_purple(),
                                          )

                    embed.add_field(name='Staffer', value=ctx.author, inline=False)
                    embed.add_field(name='Motivazione', value=reason, inline=False)
                    embed.add_field(name='Data Comando', value=get_date(), inline=False)
                    embed.add_field(name='Info sul Kick', value=data['InfoBanKick'], inline=False)
                    await member.send(embed=embed)

                embed = discord.Embed(title='Utente Espulso',
                                      description='Un utente è stato espulso dal server',
                                      color=discord.Color.dark_purple())

                embed.add_field(name='Autore Comando', value=ctx.author.mention, inline=False)
                embed.add_field(name='Utente Espulso', value=str(member.mention), inline=False)
                embed.add_field(name='Motivazione', value=reason, inline=False)
                embed.add_field(name='Data Comando', value=get_date(), inline=False)
                channel = ctx.guild.get_channel(self.log_channel_id)

                await ctx.guild.kick(member, reason=reason)

                if channel is None:
                    print(f"\n{Colors.Red}ERROR: {Colors.Reset}il canale di log non esiste, inserisci un id corretto"
                          f" nel file di configurazione")
                    return

                await channel.send(embed=embed)

        except discord.HTTPException:
            channel = ctx.guild.get_channel(self.log_channel_id)

            embed = discord.Embed(title='Errore di Comando',
                                  description=f'Impossibile eseguire il comando {data["Prefix"]}kick',
                                  color=discord.Color.dark_purple())

            embed.add_field(name='Autore Comando', value=ctx.author.mention, inline=False)
            embed.add_field(name='Data Comando', value=get_date(), inline=False)

            await ctx.guild.kick(member)
            await channel.send(embed=embed)

    @commands.command()
    @has_guild_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        try:
            if reason is not None:
                if not member.bot:
                    embed = discord.Embed(title='Messaggio dal Server',
                                          description='sei stato bannato dal server',
                                          color=discord.Color.dark_purple(),
                                          )

                    embed.add_field(name='Staffer', value=ctx.author, inline=False)
                    embed.add_field(name='Motivazione', value=reason, inline=False)
                    embed.add_field(name='Data Comando', value=get_date(), inline=False)
                    embed.add_field(name='Info sul Ban', value=data['InfoBanKick'], inline=False)

                    await member.send(embed=embed)

                embed = discord.Embed(title='Utente Bannato',
                                      description='Un utente è stato bannato dal server',
                                      color=discord.Color.dark_purple())

                embed.add_field(name='Autore Comando', value=ctx.author.mention, inline=False)
                embed.add_field(name='Utente Espulso', value=str(member.mention), inline=False)
                embed.add_field(name='Motivazione', value=reason, inline=False)
                embed.add_field(name='Data Comando', value=get_date(), inline=False)

                channel = ctx.guild.get_channel(self.log_channel_id)

                await ctx.guild.ban(member, reason=reason)

                if channel is None:
                    print(f"\n{Colors.Red}ERROR: {Colors.Reset}il canale di log non esiste, inserisci un id corretto"
                          f" nel file di configurazione")
                    return

                await channel.send(embed=embed)

        except discord.HTTPException:
            channel = ctx.guild.get_channel(self.log_channel_id)

            embed = discord.Embed(title='Errore di Comando',
                                  description=f'Impossibile eseguire il comando {data["Prefix"]}ban',
                                  color=discord.Color.dark_purple())

            embed.add_field(name='Autore Comando', value=ctx.author.mention, inline=False)
            embed.add_field(name='Data Comando', value=get_date(), inline=False)

            await ctx.guild.ban(member)
            await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Moderation(bot))
