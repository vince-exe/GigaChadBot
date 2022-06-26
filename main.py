from discord.ext import commands

from utils.utils import InitErrors, Colors

from config.config import Config

from aiohttp.client_exceptions import ClientConnectorError

from saves.saves import Saves

import discord

import platform

import asyncio


def main():
    # check if the platform is windows to change the event loop policy and avoid the RunTimeError
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # try to init the Config and Saves class
    if not (Config.init() and Saves.init()):
        exit(InitErrors.Reading_Settings_Error)

    # create a bot object that we are going to use to connect with Discord APIs
    bot = commands.Bot(command_prefix=Config.get_prefix(), help_command=None)

    #   load the extensions of the bot
    bot.load_extension('bot.moderation.moderation_commands')
    bot.load_extension('bot.interaction.interaction_commands')
    bot.load_extension('bot.errors.error_commands')

    # start the run method to connect with the Discord server
    try:
        bot.run(Config.get_token())

    except KeyboardInterrupt:
        exit(InitErrors.Key_Board_Interrupt)

    # if the token isn't valid
    except discord.errors.LoginFailure:
        print(f"\n{Colors.Red}ERROR: {Colors.Reset}Invalid token")
        exit(InitErrors.Invalid_Token)

    except ClientConnectorError:
        print(f"\n{Colors.Red}ERROR: {Colors.Reset}Can't connect to Discord")
        exit(InitErrors.Connection_Error)

    # save all the changes
    Saves.save_all()


if __name__ == '__main__':
    main()
