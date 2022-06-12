from discord.ext import commands

from utils.utils import Colors


class Iterations(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'\n{Colors.Green}--> {Colors.Reset}Iterations commands ready')

    @commands.command()
    async def hello(self, ctx):
        author = str(ctx.author)
        await ctx.send(f'Ciao {author[0:len(author) - 5]}')

    @commands.command()
    async def repeat(self, ctx, message=None):
        if message is None:
            await ctx.send('Cosa devo ripetere bro??')
        else:
            await ctx.send(ctx.message.content[len('?repeat'):])


def setup(bot):
    bot.add_cog(Iterations(bot))
