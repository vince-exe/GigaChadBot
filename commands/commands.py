from utils.enums import Colors

from utils.utils import data

import discord


#  create a client object that we are going to use to connect with Discord APIs
client = discord.Client()


@client.event
async def on_ready():
    print(f"{Colors.Green}--> {Colors.Reset}Successfully logged in as {client.user}")
