from discord.ext import commands

from discord.ext.commands import has_guild_permissions

from utils.utils import find_black_word

from bot.moderation.moderation_utils import *

from saves.saves import Saves

import discord


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.log_channel_id = Config.get_log_channel()
        self.fail_log_channel_id = Config.get_fail_log_channel()
        self.spam_log_channel_id = Config.get_spam_log_channel()

        self.black_list_status = True
        self.sleep_channels_list = []

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'\n{Colors.Green}--> {Colors.Reset}Moderation commands ready')

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            message.content = str(message.content)
            msg = message.content.lower()

            # if the channel is a DM channel, do nothing
            if isinstance(message.channel, discord.DMChannel):
                return

            # if the message is longer than the Max Message Len
            if len(message.content) > Config.get_max_message_len():
                await message.delete()
                return

            # check if the blacklist status is on
            if self.black_list_status:
                # if the message doesn't start with this strings
                if not (msg.startswith(f'{Config.get_prefix()}add_blackword') or
                        msg.startswith(f'{Config.get_prefix()}rm_blackword')):

                    # if the user said a word that is present in the blacklist and it' not an excluded user from
                    # the black list control
                    if find_black_word(Saves.get_blackwords(), msg) and not check_role(message):
                        # delete the message
                        await message.delete()

                        # send the embed message to the user
                        await send_black_word_embed(message, [self.spam_log_channel_id, self.fail_log_channel_id])
        except IndexError:
            pass

    @commands.command()
    @has_guild_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if not is_moderation_channel(ctx.channel.id):
            return

        try:
            # check if there is a reason
            if reason is not None:
                # check if the user is not a bot
                if not member.bot:
                    await member.send(embed=get_kick_embed(ctx, reason))

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
        if not is_moderation_channel(ctx.channel.id):
            return

        try:
            if reason is not None:
                if not member.bot:
                    await member.send(embed=get_ban_embed(ctx, reason))

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

    # set the blacklist status based on the given mode, Mode = "on" BlackList = True vice versa False
    @has_guild_permissions(administrator=True)
    @commands.command()
    async def set_blacklist(self, ctx, *, mode):
        if not is_moderation_channel(ctx.channel.id):
            return

        mode_ = str(mode).lower()

        # check if the status was already the status that he gave
        if (mode_ == 'on' and self.black_list_status) or (mode_ == 'off' and not self.black_list_status):
            return

        if mode_ == 'on':
            # get the channel where the bot has to send the log message
            channel = ctx.guild.get_channel(self.log_channel_id)

            if channel is not None:
                await channel.send(embed=get_blacklist_changed_embed(self.black_list_status, ctx))
            else:
                print(f'\n{Colors.Red}ERROR: {Colors.Reset}il canale di log non esiste, inserisci un id corretto'
                      f' nel file di configurazione')

            self.black_list_status = True

        elif mode_ == 'off':
            channel = ctx.guild.get_channel(self.log_channel_id)

            if channel is not None:
                await channel.send(embed=get_blacklist_changed_embed(self.black_list_status, ctx))
            else:
                print(f'\n{Colors.Red}ERROR: {Colors.Reset}il canale di log non esiste, inserisci un id corretto'
                      f' nel file di configurazione')

            self.black_list_status = False

    # return the embed with the blacklist status
    @has_guild_permissions(mute_members=True)
    @commands.command()
    async def get_blacklist(self, ctx):
        if not is_moderation_channel(ctx.channel.id):
            return

        await ctx.channel.send(embed=get_blacklist_status_embed(self.black_list_status))

    # add the given black word to the black words list
    @has_guild_permissions(administrator=True)
    @commands.command()
    async def add_blackword(self, ctx, *, black_word=None):
        if not is_moderation_channel(ctx.channel.id):
            return

        channel = ctx.guild.get_channel(self.spam_log_channel_id)

        if black_word is not None:
            # cast and transform to lower case the black_word
            black_word = str(black_word).lower()
            # check if the black_words has been added correctly
            if Saves.add_black_word(black_word):
                if channel is None:
                    print(f'{Colors.Red}ERROR: {Colors.Reset}Il canale di spam log non esiste, inserisci un id corretto'
                          f' nel file di configurazione')
                    return

                await channel.send(embed=get_add_blacklist_word_embed(ctx, black_word))
            # if the black_word already exist
            else:
                await channel.send(embed=black_word_already_exist_embed(ctx, black_word))

    # remove the given black word from the black words list
    @has_guild_permissions(administrator=True)
    @commands.command()
    async def rm_blackword(self, ctx, *, black_word):
        if not is_moderation_channel(ctx.channel.id):
            return

        channel = ctx.guild.get_channel(self.spam_log_channel_id)

        if channel is None:
            print(f'{Colors.Red}ERROR: {Colors.Reset}Il canale di spam log non esiste, inserisci un id corretto'
                  f' nel file di configurazione')
            return

        if Saves.rm_black_word(str(black_word).lower()):
            await channel.send(embed=remove_blackword_embed(ctx, black_word))
        else:
            await channel.send(embed=fail_removed_blackword_embed(ctx, black_word))

    # clear the chat based on the given number of message to clear
    @commands.command()
    @has_guild_permissions(manage_channels=True)
    async def clear_(self, ctx, limit_=None):
        if limit_ is not None and limit_ >= 1:
            await ctx.channel.purge(limit=int(limit_))

    # clear the All the chat
    @commands.command()
    @has_guild_permissions(manage_channels=True)
    async def clear(self, ctx):
        await ctx.channel.purge()


def setup(bot):
    bot.add_cog(Moderation(bot))
