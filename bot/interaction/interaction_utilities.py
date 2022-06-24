from saves.saves import Saves

from config.config import Config

import discord

from random import randint


# return all the black words
def get_blacklist_embed(ctx):
    embed = discord.Embed(title='Lista Black Words',
                          description='lista completa delle parole bandite',
                          color=discord.Color.dark_purple())

    embed.set_thumbnail(url=ctx.author.avatar_url)

    black_words = Saves.get_blackwords()
    for i in range(len(black_words)):
        embed.add_field(name=f'# {i + 1}', value=black_words[i], inline=False)

    return embed


# return all the citations
def get_citations_embed(ctx):
    embed = discord.Embed(title='Lista Citazioni',
                          description='lista completa delle citazioni del bot',
                          color=discord.Color.dark_purple())

    embed.set_thumbnail(url=ctx.author.avatar_url)

    citations_list = Saves.get_citations()
    for i in range(len(citations_list)):
        embed.add_field(name=f'# {i + 1}', value=str(citations_list[i]), inline=False)

    return embed


#  return the embed that contains all the information about a user
def get_whois_embed(member, role):
    embed = discord.Embed(title="Informazioni Utente",
                          color=discord.Color.dark_purple())

    # set the user info
    fields = [("Nome", str(member), True),
              ("ID", member.id, True),
              ("Top Ruolo", role, False),
              ("Data Creazione", member.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
              ("Entrato Nel Server", member.joined_at.strftime("%d/%m/%Y %H:%M:%S"), True),
              ]

    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)

    # set the image of the user
    embed.set_thumbnail(url=member.avatar_url)
    return embed


# return the embed that contain all the info about a channel
def get_channel_info_embed(ctx, channel: discord.abc.GuildChannel):
    embed = discord.Embed(title='Informazioni Canale',
                          color=discord.Color.dark_purple())

    # set the name of the channel
    embed.add_field(name='Nome Canale', value=str(channel), inline=False)

    # check if the channel is in a category
    if channel.category is not None:
        embed.add_field(name='Nome Categoria', value=str(channel.category), inline=False)
    else:
        embed.add_field(name='Categoria', value='Nessuna', inline=False)

    embed.set_thumbnail(url=ctx.author.avatar_url)

    # set the creation time of a channel
    embed.add_field(name='Data Creazione', value=channel.created_at.strftime("%d/%m/%Y %H:%M:%S"), inline=False)
    return embed


# return the embed that contain a citation
def get_citation_embed():
    embed = discord.Embed(title='Citazione Pescata',
                          color=discord.Color.dark_purple())

    citations = Saves.get_citations()
    rand = randint(0, len(citations) - 1)

    embed.add_field(name='Citazione', value=str(citations[rand]), inline=False)
    return embed


# return the embed that contain the list of all the commands
def get_commands_list_embed(ctx):
    embed = discord.Embed(title='Lista Comandi',
                          description='Lista di tutti i comandi che il bot dispone',
                          color=discord.Color.dark_purple())

    embed.set_thumbnail(url=ctx.author.avatar_url)

    for command in Config.commands_list.items():
        embed.add_field(name=f'{Config.get_prefix()}{command[0]}', value=command[1], inline=False)

    embed.set_footer(text=f'digita {Config.get_prefix()}help [comando] per avere informazioni specifiche su un comando')
    return embed


# return the embed that contain a specific command description
def get_specific_command_embed(ctx, command):
    embed = discord.Embed(title='Descrizione Comando',
                          color=discord.Color.dark_purple())

    embed.set_thumbnail(url=ctx.author.avatar_url)
    embed.add_field(name=command[0], value=command[1], inline=False)

    return embed


def is_interaction_channel(channel_id):
    for id_ in Config.get_interaction_channels():
        if id_ == channel_id:
            return True

    return False
