from discord.ext import commands

from utils.utils import Colors

from bot.interaction.interaction_utilities import *

from sys import maxsize

from random import randint, seed


class Interaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'\n{Colors.Green}--> {Colors.Reset}Interaction commands ready')

    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def hello(self, ctx):
        if not is_interaction_channel(ctx.channel.id):
            return

        author = str(ctx.author)
        await ctx.send(f'Ciao {author[0:len(author) - 5]}')

    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def repeat(self, ctx, message=None):
        if not is_interaction_channel(ctx.channel.id):
            return

        if message is None:
            await ctx.send('Cosa devo ripetere bro??')
        else:
            await ctx.send(ctx.message.content[len('?repeat'):])

    # return the info about a user
    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def whois(self, ctx, member: discord.Member):
        if not is_interaction_channel(ctx.channel.id):
            return

        return await ctx.send(embed=get_whois_embed(member))

    # take the id of a channel and return the channel name
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def chinfo(self, ctx, *, channel_id=None):
        if not is_interaction_channel(ctx.channel.id):
            return

        if channel_id is not None:
            channel = ctx.guild.get_channel(int(channel_id))
            if channel is not None:
                await ctx.channel.send(embed=get_channel_info_embed(ctx, channel))

    # send the black list to the message author
    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def blackwords(self, ctx):
        if not is_interaction_channel(ctx.channel.id):
            return

        try:
            # send the blacklist embed to the user
            await ctx.author.send(embed=get_blacklist_embed(ctx))

        # if the bot can't sand the message in the direct channel
        except discord.HTTPException:
            return

    # send the citation list to the message author
    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def citations(self, ctx):
        if not is_interaction_channel(ctx.channel.id):
            return

        try:
            # send the citation list embed to the user
            await ctx.author.send(embed=get_citations_embed(ctx))

        except discord.HTTPException:
            return

    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def citation(self, ctx):
        if not is_interaction_channel(ctx.channel.id):
            return

        await ctx.channel.send(embed=get_citation_embed())

    # return the description of a specific command or the commands list
    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def help(self, ctx, *, command=None):
        if not is_interaction_channel(ctx.channel.id):
            return

        # send the commands list to the message author
        if command is None:
            return await ctx.author.send(embed=get_commands_list_embed(ctx))

        # check if the command that he searched is present in the commands list
        if command in Config.commands_list.keys():
            return await ctx.channel.send(embed=get_specific_command_embed(ctx, (command,
                                                                                 Config.commands_list.get(command))))

    # return a casual number between the given numbers
    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def random(self, ctx, min_: int, max_: int):
        if not is_interaction_channel(ctx.channel.id):
            return

        # check if the numbers aren't too big or short
        if min_ < -(maxsize - 1) or max_ > maxsize:
            return await ctx.channel.send('I numeri sono troppo grandi / piccoli')

        # check if the min is greater than the max, and if so switch min and max
        if min_ > max_:
            tmp = max_
            max_ = min_
            min_ = tmp

        return await ctx.channel.send(f'{randint(min_, max_)}')

    # abbreviation of head or tails
    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def hot(self, ctx):
        if not is_interaction_channel(ctx.channel.id):
            return

        seed(randint(0, 999999))
        # 0 = head || 1 = tails
        if randint(0, 1):
            return await ctx.channel.send('É uscita testa')

        return await ctx.channel.send('É uscita croce')

    # send the pic of the message author, or if a member has been @mentioned send the pic of the member
    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def pic(self, ctx, member: discord.Member = None):
        if not is_interaction_channel(ctx.channel.id):
            return

        if member is None:
            return await ctx.channel.send(embed=get_profile_pic(ctx.author.avatar_url))

        await ctx.channel.send(embed=get_profile_pic(member.avatar_url))

    # return the number of warn of the tagged user, if no user is tagged than return the number of warn of the author
    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def warnof(self, ctx, member: discord.Member = None):
        if not is_interaction_channel(ctx.channel.id):
            return

        if member is None:
            return await ctx.channel.send(embed=get_warn_number(str(ctx.author), ctx.author.id, ctx.author.avatar_url))

        return await ctx.channel.send(embed=get_warn_number(str(member), member.id, member.avatar_url))


def setup(bot):
    bot.add_cog(Interaction(bot))
