import aiohttp.client_exceptions
from discord import Permissions

from commands.commands import *


import discord


if __name__ == '__main__':
    if not data:
        exit(GeneralErrors.ReadingSettingsError)

    #  start the run method to connect with the Discord server
    try:
        bot.run(data['Token'])

    except KeyboardInterrupt:
        exit(GeneralErrors.KeyBoardInterrupt_)

    except discord.errors.LoginFailure:
        print(f"\n{Colors.Red}ERROR: {Colors.Reset}Invalid token")
        exit(DiscordErrors.InvalidToken)

    except aiohttp.client_exceptions.ClientConnectorError:
        print(f"\n{Colors.Red}ERROR: {Colors.Reset}Can't connect to Discord")
        exit(GeneralErrors.ConnectionError_)
