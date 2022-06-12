from discord.ext import commands

from utils.enums import Colors


class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'\n{Colors.Green}--> {Colors.Reset}Errors handler ready')

    @commands.command()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            pass

        elif isinstance(error, commands.MissingPermissions):
            await ctx.send('Non hai i permessi necessari per eseguire questo comando')


def setup(bot):
    bot.add_cog(Errors(bot))
