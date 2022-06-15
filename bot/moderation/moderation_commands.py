from discord.ext import commands

from discord.ext.commands import has_guild_permissions

from utils.utils import Colors, find_black_word

from config.config import data

from bot.moderation.moderation_utils import *

import discord


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_channel_id = int(data['LogChannel'])
        self.fail_log_channel_id = int(data['FailLogChannel'])
        self.spam_log_channel_id = int(data['SpamLogChannel'])

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
                await self.send_black_word_embed(user_embed=get_black_word_user_embed(message, data),
                                                 message=message,
                                                 failed_embed=get_black_word_failed_embed(message),
                                                 log_embed=get_black_word_log_embed(message))

    @commands.command()
    @has_guild_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        try:
            # check if there is a reason
            if reason is not None:
                # check if the user is not a bot
                if not member.bot:
                    await member.send(embed=get_kick_embed(ctx, reason, data['InfoBanKick']))

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
                await channel.send(embed=get_kick_log_embed(ctx, member, reason))

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
            await channel.send(embed=get_kick_failed_embed(ctx, member))

    @commands.command()
    @has_guild_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        try:
            if reason is not None:
                if not member.bot:
                    await member.send(embed=get_ban_embed(ctx, reason, data['InfoBanKick']))

                channel = ctx.guild.get_channel(self.log_channel_id)
                await ctx.guild.ban(member, reason=reason)

                if channel is None:
                    print(f"\n{Colors.Red}ERROR: {Colors.Reset}il canale di log non esiste, inserisci un id corretto"
                          f" nel file di configurazione")
                    return

                await channel.send(embed=get_ban_log_embed(ctx, member, reason))

        except discord.HTTPException:
            channel = ctx.guild.get_channel(self.fail_log_channel_id)
            # ban the user
            await ctx.guild.ban(member)

            if channel is None:
                print(f'\n{Colors.Red}ERROR: {Colors.Reset}il canale di fail log non esiste, inserisci un id corretto'
                      f' nel file di configurazione')
                return

            # send the embed message in the fail log channel
            await channel.send(embed=get_ban_failed_embed(ctx, member))


def setup(bot):
    bot.add_cog(Moderation(bot))
