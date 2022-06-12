from discord.ext import commands

from utils.utils import data, load_ext

from utils.enums import GeneralErrors, Colors, DiscordErrors

from aiohttp.client_exceptions import ClientConnectorError

import discord


if __name__ == '__main__':
    if not data:
        exit(GeneralErrors.ReadingSettingsError)

    #  create a bot object that we are going to use to connect with Discord APIs
    bot = commands.Bot(command_prefix=data['Prefix'])

    load_ext('bot/moderation_commands', bot)
    load_ext('bot/iteration_commands', bot)
    load_ext('bot/utility_commands', bot)
    load_ext('bot/error_commands', bot)

    #  start the run method to connect with the Discord server
    try:
        bot.run(data['Token'])

    except KeyboardInterrupt:
        exit(GeneralErrors.KeyBoardInterrupt_)

    except discord.errors.LoginFailure:
        print(f"\n{Colors.Red}ERROR: {Colors.Reset}Invalid token")
        exit(DiscordErrors.InvalidToken)

    except ClientConnectorError:
        print(f"\n{Colors.Red}ERROR: {Colors.Reset}Can't connect to Discord")
        exit(GeneralErrors.ConnectionError_)
