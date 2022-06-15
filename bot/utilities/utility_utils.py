import discord


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
