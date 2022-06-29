from discord.ext import commands

from discord.ext.commands import has_guild_permissions

from utils.utils import find_black_word

from bot.moderation.moderation_utils import *

from saves.saves import Saves

import discord

import asyncio


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.log_channel_id = Config.get_log_channel()
        self.fail_log_channel_id = Config.get_fail_log_channel()
        self.spam_log_channel_id = Config.get_spam_log_channel()

        self.mute_role_id = Config.get_mute_role()

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
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if not is_moderation_channel(ctx.channel.id):
            return

        try:
            # check if there is a reason
            if reason is not None:
                # check if the user is not a bot
                if not member.bot:
                    await member.send(embed=kick_embed(ctx, reason))

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
                await channel.send(embed=kick_log_embed(ctx, member, reason))

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
            await channel.send(embed=kick_failed_embed(ctx, member))

    @commands.command()
    @has_guild_permissions(ban_members=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if not is_moderation_channel(ctx.channel.id):
            return

        try:
            if reason is not None:
                if not member.bot:
                    await member.send(embed=ban_embed(ctx, reason))

                channel = ctx.guild.get_channel(self.log_channel_id)
                await ctx.guild.ban(member, reason=reason)

                if channel is None:
                    print(f"\n{Colors.Red}ERROR: {Colors.Reset}il canale di log non esiste, inserisci un id corretto"
                          f" nel file di configurazione")
                    return

                await channel.send(embed=ban_log_embed(ctx, member, reason))

        except discord.HTTPException:
            channel = ctx.guild.get_channel(self.fail_log_channel_id)
            # ban the user
            await ctx.guild.ban(member)

            if channel is None:
                print(f'\n{Colors.Red}ERROR: {Colors.Reset}il canale di fail log non esiste, inserisci un id corretto'
                      f' nel file di configurazione')
                return

            # send the embed message in the fail log channel
            await channel.send(embed=ban_failed_embed(ctx, member))

    # set the blacklist status based on the given mode, Mode = "on" BlackList = True vice versa False
    @has_guild_permissions(administrator=True)
    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
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
                await channel.send(embed=blacklist_changed_embed(self.black_list_status, ctx))
            else:
                print(f'\n{Colors.Red}ERROR: {Colors.Reset}il canale di log non esiste, inserisci un id corretto'
                      f' nel file di configurazione')

            self.black_list_status = True

        elif mode_ == 'off':
            channel = ctx.guild.get_channel(self.log_channel_id)

            if channel is not None:
                await channel.send(embed=blacklist_changed_embed(self.black_list_status, ctx))
            else:
                print(f'\n{Colors.Red}ERROR: {Colors.Reset}il canale di log non esiste, inserisci un id corretto'
                      f' nel file di configurazione')

            self.black_list_status = False

    # return the embed with the blacklist status
    @has_guild_permissions(administrator=True)
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def get_blacklist(self, ctx):
        if not is_moderation_channel(ctx.channel.id):
            return

        await ctx.channel.send(embed=blacklist_status_embed(self.black_list_status))

    # add the given black word to the black words list
    @has_guild_permissions(administrator=True)
    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
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

                await channel.send(embed=add_blacklist_word_embed(ctx, black_word))
            # if the black_word already exist
            else:
                await channel.send(embed=black_word_already_exist_embed(ctx, black_word))

    # remove the given black word from the black words list
    @has_guild_permissions(administrator=True)
    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
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
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def clear_(self, ctx, limit_=None):
        if limit_ is not None and limit_ >= 1:
            await ctx.channel.purge(limit=int(limit_))

    # clear the All the chat
    @commands.command()
    @has_guild_permissions(manage_channels=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def clear(self, ctx):
        await ctx.channel.purge()

    # mute a user, (not the microphone)
    @has_guild_permissions(mute_members=True)
    @commands.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def mute(self, ctx, member: discord.Member, time=None, unit=None, *, reason=None):
        if not is_moderation_channel(ctx.channel.id):
            return

        try:
            if reason is None or time is None or unit is None:
                return

            unit = str(unit).lower()
            time = int(time)

            if not (unit == 's' or unit == 'm' or unit == 'h' or unit == 'd'):
                return

            role = ctx.guild.get_role(self.mute_role_id)
            if role is None:
                print(f"{Colors.Red}\nERROR: {Colors.Reset}Impossibile mutare l'utente, inserire un id corretto"
                      f" nella voce 'MuteRole' nel file di configurazione")

                fail_channel = ctx.guild.get_channel(self.fail_log_channel_id)
                if fail_channel is None:
                    print(f'{Colors.Red}\nERROR: {Colors.Reset}Il canale di fail log non esiste, inserisci un id'
                          f' corretto nel file di configurazione')

                else:
                    await fail_channel.send(embed=fail_muted_embed(ctx, member, reason, f'{time}{unit}'))
                return

            # add the mute role to the user
            await member.add_roles(role)
            log_channel = ctx.guild.get_channel(self.spam_log_channel_id)

            if log_channel is None:
                print(f'{Colors.Red}\nERROR: {Colors.Reset}Il canale di spam log non esiste, inserisci un id corretto'
                      f' nel file di configurazione')
                return

            # send the muted log
            await log_channel.send(embed=muted_log_embed(ctx, member, reason, f'{time}{unit}'))
            # send the muted message to the user
            await member.send(embed=muted_user_embed(ctx, member, reason, f'{time}{unit}'))
            # sleep the given amount of time
            await asyncio.sleep(calculate_sleep_time(unit, time))
            # remove the muted role
            await member.remove_roles(role)
            # send the unmuted log
            await log_channel.send(embed=unmuted_log_embed(ctx, member, reason, f'{time}{unit}'))

        except ValueError:
            return

        except discord.HTTPException:
            return

    # unmute a user
    @has_guild_permissions(mute_members=True)
    @commands.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def unmute(self, ctx, member: discord.Member):
        if not is_moderation_channel(ctx.channel.id):
            return

        role = ctx.guild.get_role(self.mute_role_id)

        if role is None:
            return

        channel = ctx.guild.get_channel(self.spam_log_channel_id)

        if channel is None:
            print(f'{Colors.Red}\nERROR: {Colors.Reset}Il canale di spam log non esiste, inserisci un id corretto nel'
                  f' file di configurazione')
            return

        # remove the unmuted role to the user
        await member.remove_roles(role)
        # send the log message un the log channel
        await channel.send(embed=admin_unmute_embed(ctx, member))

    # unban a user
    @has_guild_permissions(ban_members=True)
    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def unban(self, ctx, *, member):
        if not is_moderation_channel(ctx.channel.id):
            return

        banned_users = await ctx.guild.bans()

        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)

                log_channel = ctx.guild.get_channel(self.log_channel_id)
                if log_channel is None:
                    print(f'{Colors.Red}\nERROR: {Colors.Reset}il canale di log non esiste, inserisci un id '
                          f'corretto nel file di configurazione')
                    return

                await log_channel.send(embed=unban_user_embed(ctx, member))

    # return the complete banned users list
    @has_guild_permissions(ban_members=True)
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def banlist(self, ctx):
        if not is_moderation_channel(ctx.channel.id):
            return

        banned_list = await ctx.guild.bans()

        # if the list is empty, send the message to warn the admin that the list is empty
        if not len(banned_list):
            return await ctx.channel.send(embed=empty_banned_list_embed())

        await ctx.channel.send(embed=banned_list_embed(ctx, banned_list))

    # warn a user for a specific reason
    @has_guild_permissions(kick_members=True)
    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def warn(self, ctx, member: discord.Member, *, reason=None):
        if not is_moderation_channel(ctx.channel.id) or reason is None:
            return

        too_warns = False
        try:
            Saves.add_warning(member.id)

            # if the num of warnings exceeds the  'KickAfterWarns' option, then kick the user
            if Saves.get_user_warn(member.id) > Config.get_kick_after_warns():
                too_warns = True

            log_channel = ctx.guild.get_channel(self.log_channel_id)
            if log_channel is None:
                print(f'{Colors.Red}\nERROR: {Colors.Reset}il canale di log non esiste, inserisci un id corretto nel '
                      f'file di configurazione')

            # send a normal warning message to the user and in the log channel
            if not too_warns:
                if log_channel is not None:
                    # send the warning message in the log channel
                    await log_channel.send(embed=warn_log__embed(ctx, str(member), reason))

                await member.send(embed=warn_user_embed(ctx, member, reason))

            # warn the user that he has been kicked because he reached the max number of warnings
            else:
                if log_channel is not None:
                    await log_channel.send(embed=max_log_warnings_embed(ctx, member))

                # send the message to the user
                await member.send(embed=max_warnings_embed(ctx, member))

                # remove the user from the warned list, because we are going to kick it
                Saves.rm_warned_user(member.id)

                # kick the user from the server
                await ctx.guild.kick(member)

        except discord.HTTPException:
            fail_channel = ctx.guild.get_channel(self.fail_log_channel_id)

            if too_warns:
                Saves.rm_warned_user(member.id)
                await ctx.guild.kick(member)

            if fail_channel is None:
                print(f'{Colors.Red}\nERROR: {Colors.Reset}il canale di fail log non esiste, inserisci un id corretto'
                      f' nel file di configurazione')
                return

            return await fail_channel.send(embed=fail_word_embed(ctx, member, reason))

    # remove a warning from a user
    @has_guild_permissions(kick_members=True)
    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def rm_warning(self, ctx, member: discord.Member = None):
        if not is_moderation_channel(ctx.channel.id) or member is None:
            return

        # can't remove the warning from the user because he has no warnings
        match Saves.rm_warn_from_user(member.id):
            case -2:
                fail_log_channel = ctx.guild.get_channel(self.fail_log_channel_id)
                if fail_log_channel is None:
                    print(
                        f'{Colors.Red}\nERROR: {Colors.Reset}il canale di fail log non esiste, inserisci un id corretto'
                        f' nel file di configurazione')
                    return

                return await fail_log_channel.send(embed=cant_remove_warning_embed(ctx, member))

            # successfully removed the warning from the user
            case 0:
                spam_channel = ctx.guild.get_channel(self.spam_log_channel_id)
                if spam_channel is None:
                    print(f"{Colors.Red}\nERROR: {Colors.Reset}il canale di spam log non esiste, inserisci un id"
                          f" corretto nel file di configurazione")
                    return

                return await spam_channel.send(embed=rm_warning_embed(ctx, member))
                pass

    # get the warned users list
    @has_guild_permissions(kick_members=True)
    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def warned_users(self, ctx):
        if not is_moderation_channel(ctx.channel.id):
            return

        return await ctx.channel.send(embed=warned_users_embed(ctx))


def setup(bot):
    bot.add_cog(Moderation(bot))
