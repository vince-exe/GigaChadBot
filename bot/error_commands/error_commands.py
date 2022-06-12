from discord.ext import commands

from utils.utils import Colors, create_embed_error

import discord


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
            fields = [
                      ('Command Author', str(ctx.author), True),
                      ('Fail Reason', 'Non hai i permessi necessari per eseguire questo comando', True)
                     ]

            embed = create_embed_error(title='Command Error',
                                       color=discord.Color.dark_purple(),
                                       avatar_url=ctx.message.author.avatar_url,
                                       field_list=fields)

            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Errors(bot))
