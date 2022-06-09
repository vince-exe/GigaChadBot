import discord

from utils.enums import *

from utils.utils import *

from discord.ext import commands

#  create a bot object that we are going to use to connect with Discord APIs
bot = commands.Bot(command_prefix=data['Prefix'])


@bot.event
async def on_ready():
    print(f"{Colors.Green}--> {Colors.Reset}Successfully logged in as {bot.user}")


@bot.event
async def on_message(message):
    await bot.process_commands(message)


# say hello
@bot.command()
async def hello(ctx):
    author = str(ctx.author)
    await ctx.send(f'Ciao {author[0:len(author) - 5]}')


# repeat a message
@bot.command()
async def repeat(ctx, message):
    await ctx.send(message)
