from discord.ext import commands

from utils.utils import Colors

from bot.interaction.interaction_utilities import *

from discord.ext.commands import has_guild_permissions


class Interaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'\n{Colors.Green}--> {Colors.Reset}Interaction commands ready')

    @commands.command()
    async def hello(self, ctx):
        if not is_interaction_channel(ctx.channel.id):
            return

        author = str(ctx.author)
        await ctx.send(f'Ciao {author[0:len(author) - 5]}')

    @commands.command()
    async def repeat(self, ctx, message=None):
        if not is_interaction_channel(ctx.channel.id):
            return

        if message is None:
            await ctx.send('Cosa devo ripetere bro??')
        else:
            await ctx.send(ctx.message.content[len('?repeat'):])

    # return the info about a user
    @commands.command()
    async def whois(self, ctx, member: discord.Member):
        if not is_interaction_channel(ctx.channel.id):
            return

        role = str(member.top_role)
        if not role.startswith('@'):
            role = '@' + role

        await ctx.send(embed=get_whois_embed(member, role))

    # take the id of a channel and return the channel name
    @commands.command()
    @has_guild_permissions(manage_channels=True)
    async def chinfo(self, ctx, *, channel_id=None):
        if not is_interaction_channel(ctx.channel.id):
            return

        if channel_id is not None:
            channel = ctx.guild.get_channel(int(channel_id))
            if channel is not None:
                await ctx.channel.send(embed=get_channel_info_embed(ctx, channel))

    # send the black list to the message author
    @commands.command()
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
    async def citations(self, ctx):
        if not is_interaction_channel(ctx.channel.id):
            return

        try:
            # send the citation list embed to the user
            await ctx.author.send(embed=get_citations_embed(ctx))

        except discord.HTTPException:
            return


def setup(bot):
    bot.add_cog(Interaction(bot))
