from errors.errors import *

from utils.utils import read_json, data
from utils.enums import GeneralErrors, DiscordErrors

from commands.commands import *


import discord


if __name__ == '__main__':
    if not data:
        exit(GeneralErrors.ReadingSettingsError)

    #  start the run method to connect with the Discord server
    try:
        client.run(data['Token'])

    except KeyboardInterrupt:
        exit(GeneralErrors.KeyBoardInterrupt_)

    except discord.errors.LoginFailure:
        print(f"\n{Colors.Red}ERROR: {Colors.Reset}Invalid token")
        exit(DiscordErrors.InvalidToken)
