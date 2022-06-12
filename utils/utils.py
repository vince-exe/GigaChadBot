from os import listdir

import discord


class GeneralErrors:
    ReadingSettingsError = -5
    KeyBoardInterrupt_ = -1
    ValueError_ = -2
    ConnectionError_ = -3


class DiscordErrors:
    InvalidToken = -1


class Colors:
    Green = "\033[1m" + "\u001b[32m"
    Magenta = "\033[1m" + "\u001b[35m"
    Red = "\033[1m" + "\u001b[31m"
    Yellow = "\033[1m" + "\u001b[33m"
    Blu = "\033[1m" + "\033[94m"
    Reset = "\033[1m" + "\u001b[0m"


def load_ext(dir_name, bot):
    for filename in listdir(f'./{dir_name}'):
        if filename.endswith('.py'):
            bot.load_extension(f'{dir_name.replace("/", ".")}.{filename[:-3]}')


def create_embed_error(title, color, avatar_url, field_list):
    embed = discord.Embed(title=title, color=color)

    embed.set_thumbnail(url=avatar_url)

    for name, value, inline in field_list:
        embed.add_field(name=name, value=value, inline=inline)

    return embed
