import discord

from discord.ext.commands import has_guild_permissions

from utils.enums import *

from utils.utils import *

from discord.ext import commands

#  create a bot object that we are going to use to connect with Discord APIs
bot = commands.Bot(command_prefix=data['Prefix'])


@bot.event
async def on_ready():
    print(f"{Colors.Green}--> {Colors.Reset}Successfully logged in as {bot.user}")


@bot.event
async def on_message(ctx):
    try:
        await bot.process_commands(ctx)

    except discord.ext.commands.errors.CommandNotFound:
        await ctx.send(f'Il comando non è presente nel chad archivio')


# say hello
@bot.command(aliases=['ciao'])
async def hello(ctx):
    author = str(ctx.author)
    await ctx.send(f'Ciao {author[0:len(author) - 5]}')


# repeat a message
@bot.command(aliases=['ripeti'])
async def repeat(ctx, message=None):
    if message is None:
        await ctx.send('Cosa devo ripetere bro??')
    else:
        await ctx.send(ctx.message.content[len('?repeat'):])


# kick a user if he as at least the KickMembers permission
@bot.command()
@has_guild_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    if reason is None:
        await ctx.send(f'Impossibile espellere {member.mention}, devi specificare il motivo del kick!!')

    else:
        await ctx.guild.kick(member)
        await ctx.send(f"L'utente {member.mention} è stato espulso dal server per il seguente motivo: {reason}")


# handle the errors CommandNotFound, MissingPermission
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Non ho trovato il comando nel mio chad archivio')

    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('Non hai i permessi necessari')
