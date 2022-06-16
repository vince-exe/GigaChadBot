from utils.utils import get_date

import discord


# return the embed to send to the user, that worn he of the use of a black word
def get_black_word_user_embed(message, data):
    embed = discord.Embed(title='Black Word',
                          description=f"Il bot ha segnalato allo staff l'utilizzo di una black word"
                                      f" da parte tua, digita {data['Prefix']}blackwords per avere"
                                      f" la lista delle black words del server",
                          color=discord.Color.dark_purple())

    embed.add_field(name='Canale Server', value=str(message.channel.name), inline=False)
    embed.add_field(name='Id Canale', value=str(message.channel.id), inline=False)
    embed.add_field(name='Autore Messaggio', value=str(message.author), inline=False)
    embed.add_field(name='Messaggio', value=str(message.content), inline=False)

    return embed


# return the embed to send in the spam log channel
def get_black_word_log_embed(message):
    embed = discord.Embed(title='Black Word',
                          description=f'un utente ha utilizzato una black word',
                          color=discord.Color.dark_purple())

    embed.add_field(name='Canale Server', value=str(message.channel.name), inline=False)
    embed.add_field(name='Id Canale', value=str(message.channel.id), inline=False)
    embed.add_field(name='Autore Messaggio', value=str(message.author), inline=False)
    embed.add_field(name='Messaggio', value=str(message.content), inline=False)

    return embed


# return the embed to send to the user, if he got banned
def get_ban_embed(ctx, reason, info_ban_kick):
    embed = discord.Embed(title='Messaggio dal Server',
                          description='sei stato bannato dal server',
                          color=discord.Color.dark_purple(),
                          )

    embed.add_field(name='Staffer', value=ctx.author, inline=False)
    embed.add_field(name='Motivazione', value=reason, inline=False)
    embed.add_field(name='Data Comando', value=get_date(), inline=False)
    embed.add_field(name='Info sul Ban', value=info_ban_kick, inline=False)

    return embed


# return the embed to send in the fail log channel when the bot try to warn a user that used a black word
def get_black_word_failed_embed(message):
    embed = discord.Embed(title='Tentativo di Messaggio',
                          description=f"non ho potuto mandare il messaggio di warning per utilizzo di una"
                                      f" black word")

    embed.add_field(name='Autore Messaggio', value=str(message.author), inline=False)
    embed.add_field(name='Canale Server', value=str(message.channel.name), inline=False)
    embed.add_field(name='Id Canale', value=str(message.channel.id), inline=False)
    embed.add_field(name='Messaggio', value=str(message.content), inline=False)
    embed.add_field(name='Data Messaggio', value=get_date(), inline=False)

    return embed


# return the Kick Embed to send to the user
def get_kick_embed(ctx, reason, info_ban_kick):
    embed = discord.Embed(title='Messaggio dal Server',
                          description='sei stato espulso dal server',
                          color=discord.Color.dark_purple(),
                          )

    embed.add_field(name='Staffer', value=ctx.author, inline=False)
    embed.add_field(name='Motivazione', value=reason, inline=False)
    embed.add_field(name='Data Comando', value=get_date(), inline=False)
    embed.add_field(name='Info sul Kick', value=info_ban_kick, inline=False)

    return embed


# return the Kick Embed to send in the log channel
def get_kick_log_embed(ctx, member, reason):
    embed = discord.Embed(title='Utente Espulso',
                          description='Un utente è stato espulso dal server',
                          color=discord.Color.dark_purple())

    embed.add_field(name='Autore Comando', value=ctx.author, inline=False)
    embed.add_field(name='Utente Espulso', value=str(member.name), inline=False)
    embed.add_field(name='Motivazione', value=reason, inline=False)
    embed.add_field(name='Data Comando', value=get_date(), inline=False)

    return embed


# return the Ban Embed to send in the log channel
def get_ban_log_embed(ctx, member, reason):
    embed = discord.Embed(title='Utente Bannato',
                          description='Un utente è stato bannato dal server',
                          color=discord.Color.dark_purple())

    embed.add_field(name='Autore Comando', value=ctx.author, inline=False)
    embed.add_field(name='Utente Espulso', value=str(member.name), inline=False)
    embed.add_field(name='Motivazione', value=reason, inline=False)
    embed.add_field(name='Data Comando', value=get_date(), inline=False)

    return embed


# return the Fail Log Kick Embed
def get_kick_failed_embed(ctx, member):
    embed = discord.Embed(title='Tentativo di Messaggio',
                          description="Non ho potuto mandare il messaggio di kick all'utente",
                          color=discord.Color.dark_purple())

    embed.add_field(name='Autore Comando', value=ctx.author, inline=False)
    embed.add_field(name='Utente Espulso', value=member.name, inline=False)
    embed.add_field(name='Data Comando', value=get_date(), inline=False)

    return embed


# return the Fail Log Ban Embed
def get_ban_failed_embed(ctx, member):
    embed = discord.Embed(title='Tentativo di Messaggio',
                          description="Non ho potuto mandare il messaggio di ban all'utente",
                          color=discord.Color.dark_purple())

    embed.add_field(name='Autore Comando', value=ctx.author, inline=False)
    embed.add_field(name='Utente Bannato', value=member.name, inline=False)
    embed.add_field(name='Data Comando', value=get_date(), inline=False)

    return embed


# return the blacklist status
def get_blacklist_status_embed(blacklist_status):
    embed = discord.Embed(title='Stato BlackList',
                          color=discord.Color.dark_purple())

    # if the blacklist is on
    if blacklist_status:
        embed.add_field(name='Stato', value='Attiva', inline=True)
        return embed

    # if the blacklist isn't on
    embed.add_field(name='Stato', value='Disattivata', inline=True)
    return embed


def get_blacklist_changed_embed(blacklist_status_before, ctx):
    embed = discord.Embed(title='BlackList Status Modificato',
                          description='un utente ha modificato lo stato della blacklist',
                          color=discord.Color.dark_purple())

    embed.set_thumbnail(url=ctx.author.avatar_url)

    embed.add_field(name='Utente', value=str(ctx.author), inline=False)

    # set the status before and after the command

    if blacklist_status_before:
        embed.add_field(name='Stato Prima', value='Attiva', inline=False)
        embed.add_field(name='Stato Ora', value='Disattiva', inline=False)
    else:
        embed.add_field(name='Stato Prima', value='Disattiva', inline=False)
        embed.add_field(name='Stato Ora', value='Attiva', inline=False)

    # set the date and the channel where the command has been executed
    embed.add_field(name='Data Comando', value=get_date(), inline=False)
    embed.add_field(name='Canale Esecuzione', value=str(ctx.channel.name), inline=False)
    embed.add_field(name='Id Canale', value=str(ctx.channel.id), inline=False)

    return embed
