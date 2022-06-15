from discord.ext import commands

from utils.utils import Colors


class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'\n{Colors.Green}--> {Colors.Reset}Errors handler ready')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            pass

        elif isinstance(error, commands.MissingPermissions):
            pass


def setup(bot):
    bot.add_cog(Errors(bot))
