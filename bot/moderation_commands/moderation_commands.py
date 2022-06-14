from discord.ext import commands

from discord.ext.commands import has_guild_permissions

from utils.utils import Colors, find_black_word

from config.config import data

from utils.utils import get_date

import discord


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_channel_id = int(data['LogChannel'])
        self.fail_log_channel_id = int(data['FailLogChannel'])
        self.spam_log_channel_id = int(data['SpamLogChannel'])

    # return the embed to send to the user, thar worn he of the use of a black word
    @staticmethod
    def get_blacklist_user_embed(message):
        embed = discord.Embed(title='Black Word',
                              description=f"Il bot ha segnalato allo staff l'utilizzo di una black word"
                                          f" da parte tua, digita {data['Prefix']}blackwords per avere"
                                          f" la lista delle black words del server",
                              color=discord.Color.dark_purple())

        embed.add_field(name='Canale Server', value=str(message.channel.name), inline=False)
        embed.add_field(name='Autore Messaggio', value=str(message.author), inline=False)
        embed.add_field(name='Messaggio', value=str(message.content), inline=False)

        return embed

    # return the embed to send in the spam log channel
    @staticmethod
    def get_blacklist_log_embed(message):
        embed = discord.Embed(title='Black Word',
                              description=f'un utente ha utilizzato una black word',
                              color=discord.Color.dark_purple())

        embed.add_field(name='Canale Server', value=str(message.channel.name), inline=False)
        embed.add_field(name='Autore Messaggio', value=str(message.author.mention), inline=False)
        embed.add_field(name='Messaggio', value=str(message.content), inline=False)

        return embed

    # return the embed to send to the user, if he got banned
    @staticmethod
    def get_ban_embed(ctx, reason):
        embed = discord.Embed(title='Messaggio dal Server',
                              description='sei stato bannato dal server',
                              color=discord.Color.dark_purple(),
                              )

        embed.add_field(name='Staffer', value=ctx.author, inline=False)
        embed.add_field(name='Motivazione', value=reason, inline=False)
        embed.add_field(name='Data Comando', value=get_date(), inline=False)
        embed.add_field(name='Info sul Ban', value=data['InfoBanKick'], inline=False)

        return embed

    # return the embed to send in the fail log channel when the bot try to warn a user that used a black word
    @staticmethod
    def get_blacklist_failed_embed(message):
        embed = discord.Embed(title='Tentativo di Messaggio',
                              description=f"non ho potuto mandare il messaggio di warning per utilizzo di una"
                                          f" black word all'utente")

        embed.add_field(name='Utente', value=str(message.author.mention), inline=False)
        embed.add_field(name='Messaggio', value=str(message.content), inline=False)

        return embed

    # return the Kick Embed to send to the user if it's possible
    @staticmethod
    def get_kick_embed(ctx, reason):
        embed = discord.Embed(title='Messaggio dal Server',
                              description='sei stato espulso dal server',
                              color=discord.Color.dark_purple(),
                              )

        embed.add_field(name='Staffer', value=ctx.author, inline=False)
        embed.add_field(name='Motivazione', value=reason, inline=False)
        embed.add_field(name='Data Comando', value=get_date(), inline=False)
        embed.add_field(name='Info sul Kick', value=data['InfoBanKick'], inline=False)

        return embed

    # return the Kick Embed to send in the log channel
    @staticmethod
    def get_kick_log_embed(ctx, member, reason):
        embed = discord.Embed(title='Utente Espulso',
                              description='Un utente è stato espulso dal server',
                              color=discord.Color.dark_purple())

        embed.add_field(name='Autore Comando', value=ctx.author.mention, inline=False)
        embed.add_field(name='Utente Espulso', value=str(member.mention), inline=False)
        embed.add_field(name='Motivazione', value=reason, inline=False)
        embed.add_field(name='Data Comando', value=get_date(), inline=False)

        return embed

    # return the Ban Embed to send in the log channel
    @staticmethod
    def get_ban_log_embed(ctx, member, reason):
        embed = discord.Embed(title='Utente Bannato',
                              description='Un utente è stato bannato dal server',
                              color=discord.Color.dark_purple())

        embed.add_field(name='Autore Comando', value=ctx.author.mention, inline=False)
        embed.add_field(name='Utente Espulso', value=str(member.mention), inline=False)
        embed.add_field(name='Motivazione', value=reason, inline=False)
        embed.add_field(name='Data Comando', value=get_date(), inline=False)

        return embed

    # return the Fail Log Kick Embed
    @staticmethod
    def get_kick_failed_embed(ctx, member):
        embed = discord.Embed(title='Tentativo di Messaggio',
                              description="Non ho potuto mandare il messaggio di kick all'utente",
                              color=discord.Color.dark_purple())

        embed.add_field(name='Autore Comando', value=ctx.author.mention, inline=False)
        embed.add_field(name='Utente Espulso', value=member.mention, inline=False)
        embed.add_field(name='Data Comando', value=get_date(), inline=False)

        return embed

    # return the Fail Log Ban Embed
    @staticmethod
    def get_ban_failed_embed(ctx, member):
        embed = discord.Embed(title='Tentativo di Messaggio',
                              description="Non ho potuto mandare il messaggio di ban all'utente",
                              color=discord.Color.dark_purple())

        embed.add_field(name='Autore Comando', value=ctx.author.mention, inline=False)
        embed.add_field(name='Utente Bannato', value=member.mention, inline=False)
        embed.add_field(name='Data Comando', value=get_date(), inline=False)

        return embed

    async def send_black_word_embed(self, user_embed, message, failed_embed, log_embed):
        try:
            # try to send the embed message to the user
            await message.author.send(embed=user_embed)

            channel = message.guild.get_channel(self.spam_log_channel_id)

            # check if the channel is none
            if channel is None:
                print(f'\n{Colors.Red}ERROR: {Colors.Reset}il canale di spam logo non esiste, inserisci un id corretto '
                      f' nel file di configurazione')
                return

            await channel.send(embed=log_embed)

        # send the embed to the fail log channel
        except discord.HTTPException:
            # get the channel where the bot has to send the fail logs
            channel = message.guild.get_channel(self.fail_log_channel_id)

            # if the channel doesn't exist
            if channel is None:
                print(f'\n{Colors.Red}ERROR: {Colors.Reset}il canale di fail log non esiste, inserisci un id corretto'
                      f' nel file di configurazione')
                return

            # if the channel exist, send the fail log message, into the channel
            await channel.send(embed=failed_embed)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'\n{Colors.Green}--> {Colors.Reset}Moderation commands ready')

    @commands.Cog.listener()
    async def on_message(self, message):
        message.content = str(message.content)

        msg = message.content.lower()
        
        if not msg.startswith(f'{data["Prefix"]}clear') or msg.startswith(f'{data["Prefix"]}clear_'):
            # if the user said a word that is present in the blacklist
            if find_black_word(data['BlackWords'], msg):
                # delete the message
                await message.delete()

                # send the embed message to the user
                await self.send_black_word_embed(user_embed=Moderation.get_blacklist_user_embed(message), message=message,
                                                 failed_embed=Moderation.get_blacklist_failed_embed(message),
                                                 log_embed=Moderation.get_blacklist_log_embed(message))

    @commands.command()
    @has_guild_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        try:
            # check if there is a reason
            if reason is not None:
                # check if the user is not a bot
                if not member.bot:
                    await member.send(embed=Moderation.get_kick_embed(ctx, reason))

                # get the log channel
                channel = ctx.guild.get_channel(self.log_channel_id)
                # kick the user
                await ctx.guild.kick(member, reason=reason)

                # check if the log channel exist
                if channel is None:
                    print(f"\n{Colors.Red}ERROR: {Colors.Reset}il canale di log non esiste, inserisci un id corretto"
                          f" nel file di configurazione")
                    return

                # send the embed log to the log channel
                await channel.send(embed=Moderation.get_kick_log_embed(ctx, member, reason))

        except discord.HTTPException:
            # get the fail log channel
            channel = ctx.guild.get_channel(self.fail_log_channel_id)

            # check if the fail log channel exist
            if channel is None:
                print(f"\n{Colors.Red}ERROR: {Colors.Reset}il canale di fail log non esiste, inserisci un id corretto"
                      f" nel file di configurazione")
                return

            # kick the user
            await ctx.guild.kick(member)
            # send the message to the fail log channel
            await channel.send(embed=Moderation.get_kick_failed_embed(ctx, member))

    @commands.command()
    @has_guild_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        try:
            if reason is not None:
                if not member.bot:
                    await member.send(embed=Moderation.get_ban_embed(ctx, reason))

                channel = ctx.guild.get_channel(self.log_channel_id)
                await ctx.guild.ban(member, reason=reason)

                if channel is None:
                    print(f"\n{Colors.Red}ERROR: {Colors.Reset}il canale di log non esiste, inserisci un id corretto"
                          f" nel file di configurazione")
                    return

                await channel.send(embed=Moderation.get_ban_log_embed(ctx, member, reason))

        except discord.HTTPException:
            channel = ctx.guild.get_channel(self.fail_log_channel_id)
            # ban the user
            await ctx.guild.ban(member)

            if channel is None:
                print(f'\n{Colors.Red}ERROR: {Colors.Reset}il canale di fail log non esiste, inserisci un id corretto'
                      f' nel file di configurazione')
                return

            # send the embed message in the fail log channel
            await channel.send(embed=Moderation.get_ban_failed_embed(ctx, member))


def setup(bot):
    bot.add_cog(Moderation(bot))
