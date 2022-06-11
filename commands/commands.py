from discord.ext.commands import has_guild_permissions

from utils.enums import Colors

from utils.utils import data

from discord.ext import commands

import discord


#  create a bot object that we are going to use to connect with Discord APIs
bot = commands.Bot(command_prefix=data['Prefix'])


@bot.event
async def on_ready():
    print(f"\n{Colors.Green}--> {Colors.Reset}Successfully logged in as {bot.user}")


@bot.event
async def on_message(ctx):
    try:
        await bot.process_commands(ctx)

    except discord.ext.commands.errors.CommandNotFound:
        await ctx.send(f'Il comando non è presente nel chad archivio')


# Say Hello
@bot.command()
async def hello(ctx):
    author = str(ctx.author)
    await ctx.send(f'Ciao {author[0:len(author) - 5]}')


# Repeat a Message
@bot.command()
async def repeat(ctx, message=None):
    if message is None:
        await ctx.send('Cosa devo ripetere bro??')
    else:
        await ctx.send(ctx.message.content[len('?repeat'):])


# kick a user
@bot.command()
@has_guild_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    if reason is None:
        await ctx.send(f'Impossibile espellere {member.mention}, devi specificare il motivo del kick!!')

    else:
        await ctx.guild.kick(member, reason=reason)
        await ctx.send(f"L'utente {member.mention} è stato espulso dal server per il seguente motivo: {reason}")


# ban a user
@bot.command()
@has_guild_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    if reason is None:
        await ctx.send(f"Impossibile bannare {member.mention}, devi specificare il motivo del ban!!")

    else:
        await member.send(f'Sei stato bannato dal server per il seguente motivo: {reason}')
        await ctx.guild.ban(member, reason=reason)
        await ctx.channel.send(f"L'utente è stato bannato dal server da {ctx.author}")


# Clear the chat, the user pass the amount of messages that he wants to delete
@bot.command()
@has_guild_permissions(manage_channels=True)
async def clear_(ctx, limit_=None):
    if limit_ is None:
        await ctx.send(f'Parametri insufficienti, digita {data["Prefix"]}help per maggiori informazioni')

    else:
        await ctx.channel.purge(limit=int(limit_))


# Clear the All the chat
@bot.command()
@has_guild_permissions(manage_channels=True)
async def clear(ctx):
    await ctx.channel.purge()


@bot.command()
async def whois(ctx, member: discord.Member):
    embed = discord.Embed(title="Informazioni Utente",
                          color=discord.Color.dark_blue())

    fields = [("Nome", str(member), True),
              ("ID", member.id, True),
              ("Top Ruolo", f'@{member.top_role}', False),
              ("Data Creazione", member.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
              ("Entrato Nel Server", member.joined_at.strftime("%d/%m/%Y %H:%M:%S"), True),
              ]

    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)

    embed.set_thumbnail(url=member.avatar_url)
    await ctx.send(embed=embed)


# handle the errors CommandNotFound, MissingPermission
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        pass

    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('Non hai i permessi necessari per eseguire questo comando')
