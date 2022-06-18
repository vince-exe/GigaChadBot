from saves.saves import Saves

from config.config import Config

import discord


# return all the black words
def get_blacklist_embed(ctx):
    embed = discord.Embed(title='Lista Black Words',
                          description='lista completa delle parole bandite',
                          color=discord.Color.dark_purple())

    embed.set_thumbnail(url=ctx.author.avatar_url)

    black_words_counter = 1
    for black_word in Saves.get_blackwords():
        embed.add_field(name=f'# {black_words_counter}', value=black_word, inline=False)
        black_words_counter += 1

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


def is_interaction_channel(channel_id):
    for id_ in Config.get_interaction_channels():
        if id_ == channel_id:
            return True

    return False
