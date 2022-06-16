from discord.ext import commands

from utils.utils import InitErrors, Colors

from config.config import Config

from aiohttp.client_exceptions import ClientConnectorError

from saves.saves import Saves

import discord


if __name__ == '__main__':
    # try to init the Config class
    if not Config.init():
        exit(InitErrors.Reading_Settings_Error)

    if Saves.black_words_json is None:
        exit(InitErrors.Reading_Settings_Error)

    #  create a bot object that we are going to use to connect with Discord APIs
    bot = commands.Bot(command_prefix=Config.get_prefix())

    # load the extensions of the bot
    bot.load_extension('bot.moderation.moderation_commands')
    bot.load_extension('bot.interaction.interaction_commands')
    bot.load_extension('bot.utilities.utility_commands')
    bot.load_extension('bot.errors.error_commands')

    #  start the run method to connect with the Discord server
    try:
        bot.run(Config.get_token())

    except KeyboardInterrupt:
        exit(InitErrors.Key_Board_Interrupt)

    except discord.errors.LoginFailure:
        print(f"\n{Colors.Red}ERROR: {Colors.Reset}Invalid token")
        exit(InitErrors.Invalid_Token)

    except ClientConnectorError:
        print(f"\n{Colors.Red}ERROR: {Colors.Reset}Can't connect to Discord")
        exit(InitErrors.Connection_Error)
