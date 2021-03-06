from utils.utils import get_date

from config.config import Config

from utils.utils import Colors

from saves.saves import Saves

import discord


async def send_black_word_embed(message, log_channels):
    try:
        # try to send the embed message to the user
        await message.author.send(embed=black_word_user_embed(message))

        # get the spam log channel
        channel = message.guild.get_channel(log_channels[0])

        # check if the channel is none
        if channel is None:
            print(f'\n{Colors.Red}ERROR: {Colors.Reset}il canale di spam logo non esiste, inserisci un id corretto '
                  f' nel file di configurazione')
            return

        await channel.send(embed=black_word_log_embed(message))

    # send the embed to the fail log channel
    except discord.HTTPException:
        # get the channel where the bot has to send the fail logs
        channel = message.guild.get_channel(log_channels[1])

        # if the channel doesn't exist
        if channel is None:
            print(f'\n{Colors.Red}ERROR: {Colors.Reset}il canale di fail log non esiste, inserisci un id corretto'
                  f' nel file di configurazione')
            return

        # if the channel exist, send the fail log message, into the channel
        await channel.send(embed=black_word_failed_embed(message))


# return the embed to send to the user, that worn he of the use of a black word
def black_word_user_embed(message):
    embed = discord.Embed(title='Black Word',
                          description=f"Il bot ha segnalato allo staff l'utilizzo di una black word"
                                      f" da parte tua nel server digita {Config.get_prefix()}blackwords per avere"
                                      f" la lista delle black words del server",
                          color=discord.Color.dark_purple())

    embed.add_field(name='Autore Messaggio', value=str(message.author), inline=False)
    embed.add_field(name='Messaggio', value=str(message.content), inline=False)
    embed.add_field(name='Canale Server', value=str(message.channel.name), inline=False)
    embed.add_field(name='Id Canale', value=str(message.channel.id), inline=False)
    embed.add_field(name='Data Messaggio', value=get_date(), inline=False)

    return embed


# return the embed to send in the spam log channel
def black_word_log_embed(message):
    embed = discord.Embed(title='Black Word',
                          description=f'un utente ha utilizzato una black word',
                          color=discord.Color.dark_purple())

    embed.add_field(name='Autore Messaggio', value=str(message.author), inline=False)
    embed.add_field(name='Messaggio', value=str(message.content), inline=False)
    embed.add_field(name='Canale Server', value=str(message.channel.name), inline=False)
    embed.add_field(name='Id Canale', value=str(message.channel.id), inline=False)
    embed.add_field(name='Data Messaggio', value=get_date(), inline=False)

    return embed


# return the embed to send to the user, if he got banned
def ban_embed(ctx, reason):
    embed = discord.Embed(title='Messaggio dal Server',
                          description=f'sei stato bannato dal server {ctx.guild.name}',
                          color=discord.Color.dark_purple(),
                          )

    embed.add_field(name='Staffer', value=ctx.author, inline=False)
    embed.add_field(name='Motivazione', value=reason, inline=False)
    embed.add_field(name='Data Comando', value=get_date(), inline=False)
    embed.add_field(name='Info sul Ban', value=Config.get_info_ban_kick(), inline=False)

    return embed


# return the embed to send in the fail log channel when the bot try to warn a user that used a black word
def black_word_failed_embed(message):
    embed = discord.Embed(title='Tentativo di Messaggio',
                          description=f"non ho potuto mandare il messaggio di warning per utilizzo di una"
                                      f" black word ad un utente")

    embed.add_field(name='Autore Messaggio', value=str(message.author), inline=False)
    embed.add_field(name='Messaggio', value=str(message.content), inline=False)
    embed.add_field(name='Canale Server', value=str(message.channel.name), inline=False)
    embed.add_field(name='Id Canale', value=str(message.channel.id), inline=False)
    embed.add_field(name='Data Messaggio', value=get_date(), inline=False)

    return embed


# return the Kick Embed to send to the user
def kick_embed(ctx, reason):
    embed = discord.Embed(title='Messaggio dal Server',
                          description=f'sei stato espulso dal server {ctx.guild.name}',
                          color=discord.Color.dark_purple(),
                          )

    embed.add_field(name='Staffer', value=ctx.author, inline=False)
    embed.add_field(name='Motivazione', value=reason, inline=False)
    embed.add_field(name='Data Comando', value=get_date(), inline=False)
    embed.add_field(name='Info sul Kick', value=Config.get_info_ban_kick(), inline=False)

    return embed


# return the Kick Embed to send in the log channel
def kick_log_embed(ctx, member, reason):
    embed = discord.Embed(title='Utente Espulso',
                          description=f'Un utente ?? stato espulso dal server {ctx.guild.name}',
                          color=discord.Color.dark_purple())

    embed.add_field(name='Autore Comando', value=ctx.author, inline=False)
    embed.add_field(name='Utente Espulso', value=str(member.name), inline=False)
    embed.add_field(name='Motivazione', value=reason, inline=False)
    embed.add_field(name='Data Comando', value=get_date(), inline=False)

    return embed


# return the Ban Embed to send in the log channel
def ban_log_embed(ctx, member, reason):
    embed = discord.Embed(title='Utente Bannato',
                          description=f'Un utente ?? stato bannato dal server {ctx.guild.name}',
                          color=discord.Color.dark_purple())

    embed.add_field(name='Autore Comando', value=ctx.author, inline=False)
    embed.add_field(name='Utente Espulso', value=str(member.name), inline=False)
    embed.add_field(name='Motivazione', value=reason, inline=False)
    embed.add_field(name='Data Comando', value=get_date(), inline=False)

    return embed


# return the Fail Log Kick Embed
def kick_failed_embed(ctx, member):
    embed = discord.Embed(title='Tentativo di Messaggio',
                          description="Non ho potuto mandare il messaggio di kick all'utente",
                          color=discord.Color.dark_purple())

    embed.add_field(name='Autore Comando', value=ctx.author, inline=False)
    embed.add_field(name='Utente Espulso', value=member.name, inline=False)
    embed.add_field(name='Data Comando', value=get_date(), inline=False)

    return embed


# return the Fail Log Ban Embed
def ban_failed_embed(ctx, member):
    embed = discord.Embed(title='Tentativo di Messaggio',
                          description="Non ho potuto mandare il messaggio di ban all'utente",
                          color=discord.Color.dark_purple())

    embed.add_field(name='Autore Comando', value=ctx.author, inline=False)
    embed.add_field(name='Utente Bannato', value=member.name, inline=False)
    embed.add_field(name='Data Comando', value=get_date(), inline=False)

    return embed


# return the blacklist status
def blacklist_status_embed(blacklist_status):
    embed = discord.Embed(title='Stato BlackList',
                          color=discord.Color.dark_purple())

    # if the blacklist is on
    if blacklist_status:
        embed.add_field(name='Stato', value='Attiva', inline=True)
        return embed

    # if the blacklist isn't on
    embed.add_field(name='Stato', value='Disattivata', inline=True)
    return embed


# return the embed when a user change the blacklist status
def blacklist_changed_embed(blacklist_status_before, ctx):
    embed = discord.Embed(title='BlackList Status Modificato',
                          description='uno staffer ha modificato lo stato della blacklist',
                          color=discord.Color.dark_purple())

    embed.set_thumbnail(url=ctx.author.avatar_url)

    embed.add_field(name='Utente', value=str(ctx.author), inline=False)

    # set the status before and after the command

    if blacklist_status_before:
        embed.add_field(name='Stato Prima', value='Attiva', inline=False)
        embed.add_field(name='Stato Ora', value='Disattiva', inline=False)
    else:
        embed.add_field(name='Stato Prima', value='Disattiva', inline=False)
        embed.add_field(name='Stato Ora', value='Attiva', inline=False)

    # set the date and the channel where the command has been executed
    embed.add_field(name='Data Comando', value=get_date(), inline=False)
    embed.add_field(name='Canale Executions', value=str(ctx.channel.name), inline=False)
    embed.add_field(name='Id Canale', value=str(ctx.channel.id), inline=False)

    return embed


# return the embed, when an administrator add a new black_word to the black_words_list
def add_blacklist_word_embed(ctx, black_word: str):
    embed = discord.Embed(title='Nuova Black Word',
                          description='un amministratore ha aggiunto una nuova parola bandita',
                          color=discord.Color.dark_purple())

    embed.set_thumbnail(url=ctx.author.avatar_url)

    embed.add_field(name='Utente', value=str(ctx.author), inline=False)
    embed.add_field(name='Black Word', value=black_word, inline=False)
    embed.add_field(name='Canale', value=str(ctx.channel.name), inline=False)
    embed.add_field(name='Id Canale', value=str(ctx.channel.id), inline=False)
    embed.add_field(name='Data Comando', value=get_date(), inline=False)

    return embed


# return the embed, when an administrator try to add a black_word that already exist
def black_word_already_exist_embed(ctx, black_word: str):
    embed = discord.Embed(title='Tentativo Inserimento Black Word',
                          description='un amministratore ha cercato di aggiungere una black word',
                          color=discord.Color.dark_purple())

    embed.set_thumbnail(url=ctx.author.avatar_url)

    embed.add_field(name='Utente', value=str(ctx.author), inline=False)
    embed.add_field(name='Black Word', value=black_word, inline=False)
    embed.add_field(name='Canale', value=str(ctx.channel.name), inline=False)
    embed.add_field(name='Id Canale', value=str(ctx.channel.id), inline=False)
    embed.add_field(name='Data Comando', value=get_date(), inline=False)
    embed.add_field(name='Motivo Fallimento', value="La black word ?? gi?? presente all'interno della black words lista",
                    inline=False)

    return embed


# return the embed, when the administrator remove a black word from the black list
def remove_blackword_embed(ctx, black_word: str):
    embed = discord.Embed(title='Black Word Rimossa',
                          description='un amministratore ha rimosso una black word',
                          color=discord.Color.dark_purple())

    embed.set_thumbnail(url=ctx.author.avatar_url)

    embed.add_field(name='Utente', value=str(ctx.author), inline=False)
    embed.add_field(name='Black Word Rimossa', value=black_word, inline=False)
    embed.add_field(name='Canale', value=str(ctx.channel.name), inline=False)
    embed.add_field(name='Id Canale', value=str(ctx.channel.id), inline=False)
    embed.add_field(name='Data Comando', value=get_date(), inline=False)

    return embed


# return the embed, when the administrator try to remove an inexistent black word from the black list
def fail_removed_blackword_embed(ctx, black_word: str):
    embed = discord.Embed(title='Tentativo Rimozione Black Word',
                          description='un amministratore ha cercato di rimuovere una black word',
                          color=discord.Color.dark_purple())

    embed.set_thumbnail(url=ctx.author.avatar_url)

    embed.add_field(name='Utente', value=str(ctx.author), inline=False)
    embed.add_field(name='Black Word', value=black_word, inline=False)
    embed.add_field(name='Canale', value=str(ctx.channel.name), inline=False)
    embed.add_field(name='Id Canale', value=str(ctx.channel.id), inline=False)
    embed.add_field(name='Data Comando', value=get_date(), inline=False)
    embed.add_field(name='Motivo Fallimento', value='La black word non esiste', inline=False)

    return embed


# return the embed, when a user went muted
def muted_log_embed(ctx, user, reason, muted_time):
    embed = discord.Embed(title='Utente Mutato',
                          description='un utente ?? stato mutato da uno staffer',
                          color=discord.Color.dark_purple()
                          )

    embed.set_thumbnail(url=ctx.author.avatar_url)

    embed.add_field(name='Staffer', value=str(ctx.author), inline=False)
    embed.add_field(name='Motivazione', value=reason, inline=False)
    embed.add_field(name='Utente', value=str(user), inline=False)
    embed.add_field(name='Data Comando', value=get_date(), inline=False)
    embed.add_field(name='Durata Mute', value=muted_time, inline=False)
    return embed


# return the embed, when a staffer try to mute a user, but the command went wrong
def fail_muted_embed(ctx, user, reason, muted_time):
    embed = discord.Embed(title='Tentativo Di Mute',
                          description='uno staffer ha tentato di mutare un utente',
                          color=discord.Color.dark_purple()
                          )

    embed.set_thumbnail(url=ctx.author.avatar_url)

    embed.add_field(name='Staffer', value=str(ctx.author), inline=False)
    embed.add_field(name='Motivazione', value=reason, inline=False)
    embed.add_field(name='Utente', value=str(user), inline=False)
    embed.add_field(name='Data Comando', value=get_date(), inline=False)
    embed.add_field(name='Durata Mute', value=muted_time, inline=False)
    embed.add_field(name='Motivo Fail', value="Id del ruolo mute incorretto, contattare il gestore del bot",
                    inline=False)

    return embed


# return the embed that warn the user that he has been muted
def muted_user_embed(ctx, user, reason, muted_time):
    embed = discord.Embed(title='Sei Stato Mutato',
                          description='uno staffer ti ha mutato',
                          color=discord.Color.dark_purple()
                          )

    embed.set_thumbnail(url=ctx.author.avatar_url)

    embed.add_field(name='Staffer', value=str(ctx.author), inline=False)
    embed.add_field(name='Motivazione', value=reason, inline=False)
    embed.add_field(name='Utente', value=str(user), inline=False)
    embed.add_field(name='Data Comando', value=get_date(), inline=False)
    embed.add_field(name='Durata Mute', value=muted_time, inline=False)

    embed.set_footer(text='aspetta la fine della durata del mute per poter scrivere')
    return embed


# return the embed when a user went unmuted (by time)
def unmuted_log_embed(ctx, user, reason, muted_time):
    embed = discord.Embed(title='Utente Smutato',
                          description="un utente ?? stato smutato",
                          color=discord.Color.dark_purple()
                          )

    embed.set_thumbnail(url=ctx.author.avatar_url)

    embed.add_field(name='Staffer', value=str(ctx.author), inline=False)
    embed.add_field(name='Motivazione', value=reason, inline=False)
    embed.add_field(name='Utente', value=str(user), inline=False)
    embed.add_field(name='Data Comando', value=get_date(), inline=False)
    embed.add_field(name='Durata Mute', value=muted_time, inline=False)

    return embed


# return the embed when an admin unmute a member with the ('Prefix'unmute) command (so not by time)
def admin_unmute_embed(ctx, user):
    embed = discord.Embed(title='Admin Ha Smutato Utente',
                          description=f'un admin ha usato il comando {Config.get_prefix()}unmute per smutare un utente',
                          color=discord.Color.dark_purple())

    embed.set_thumbnail(url=ctx.author.avatar_url)

    embed.add_field(name='Admin', value=str(ctx.author), inline=False)
    embed.add_field(name='Utente', value=str(user), inline=False)
    embed.add_field(name='Data Comando', value=get_date(), inline=False)

    return embed


# return the embed when a user get unbanned
def unban_user_embed(ctx, member):
    embed = discord.Embed(title='Utente Sbannato',
                          description='un admin ha sbannato un utente',
                          color=discord.Color.dark_purple())

    embed.set_thumbnail(url=ctx.author.avatar_url)

    embed.add_field(name='Admin', value=str(ctx.author), inline=False)
    embed.add_field(name='Utente', value=str(member), inline=False)
    embed.add_field(name='Data Comando', value=get_date(), inline=False)

    return embed


# return the embed of the complete banned users list
def banned_list_embed(ctx, banned_list):
    embed = discord.Embed(title='Lista Utenti Bannati',
                          description='lista completi degli utenti bannati dal server',
                          color=discord.Color.dark_purple())

    embed.set_thumbnail(url=ctx.author.avatar_url)

    i = 0
    for user in banned_list:
        embed.add_field(name=f'# {i + 1}', value=f'{user[1] }', inline=False)
        i += 1

    return embed


# return the embed when the banned list is empty
def empty_banned_list_embed():
    embed = discord.Embed(title='Lista Utenti Bannati',
                          description='la lista degli utenti bannati ?? vuota',
                          color=discord.Color.dark_purple())

    return embed


# return the embed when the user get warned
def warn_log__embed(ctx, member, reason):
    embed = discord.Embed(title='Utente Warnato',
                          description='uno staffer ha warnato un utente',
                          color=discord.Color.dark_purple())

    embed.set_thumbnail(url=ctx.author.avatar_url)

    embed.add_field(name='Staffer', value=ctx.author, inline=False)
    embed.add_field(name='Motivazione', value=reason, inline=False)
    embed.add_field(name='Utente', value=member, inline=False)
    embed.add_field(name='Data Comando', value=get_date(), inline=False)

    return embed


# return the embed to the warned user
def warn_user_embed(ctx, member, reason):
    embed = discord.Embed(title='Sei Stato Warnato',
                          description='uno staffer ti ha warnato',
                          color=discord.Color.dark_purple())

    embed.set_thumbnail(url=ctx.author.avatar_url)

    embed.add_field(name='Staffer', value=ctx.author, inline=False)
    embed.add_field(name='Motivazione', value=reason, inline=False)
    embed.add_field(name='Utente', value=str(member), inline=False)
    embed.add_field(name='Data Comando', value=get_date(), inline=False)
    embed.add_field(name='Server', value=ctx.guild.name, inline=False)

    return embed


# return the embed when the bot could not send the message to the user
def fail_word_embed(ctx, member, reason):
    embed = discord.Embed(title='Tentativo Avviso Warn Utente',
                          description="il bot ha tentato di mandare un messaggio di warn all'utente",
                          color=discord.Color.dark_purple())

    embed.set_thumbnail(url=ctx.author.avatar_url)

    embed.add_field(name='Staffer', value=ctx.author, inline=False)
    embed.add_field(name='Motivazione', value=reason, inline=False)
    embed.add_field(name='Utente', value=str(member), inline=False)
    embed.add_field(name='Data Comando', value=get_date(), inline=False)

    return embed


# return the embed when a user reach the max number of warnings in the server
def max_warnings_embed(ctx, member):
    embed = discord.Embed(title='Sei Stato Espulso',
                          description=f'sei stato espulso dal server {ctx.guild.name}',
                          color=discord.Color.dark_purple())

    embed.set_thumbnail(url=ctx.author.avatar_url)

    embed.add_field(name='Staffer', value=str(ctx.author), inline=False)
    embed.add_field(name='Utente', value=str(member), inline=False)
    embed.add_field(name='Motivazione', value='Numero massimo di warnings raggiunti', inline=False)
    embed.add_field(name='Tuoi Warnings', value=str(Saves.get_user_warn(member.id)), inline=False)
    embed.add_field(name='Consentiti Dal Server', value=str(Config.get_kick_after_warns()), inline=False)
    embed.add_field(name='Data Comando', value=get_date(), inline=False)
    embed.add_field(name='Info Kick', value=str(Config.get_info_ban_kick()), inline=False)

    return embed


# return the embed in the log channel when a user reach the max num of warnings
def max_log_warnings_embed(ctx, member):
    embed = discord.Embed(title='Utente Espulso',
                          description=f'un utente ?? stato espulso dal server',
                          color=discord.Color.dark_purple())

    embed.set_thumbnail(url=ctx.author.avatar_url)

    embed.add_field(name='Staffer', value=str(ctx.author), inline=False)
    embed.add_field(name='Utente', value=str(member), inline=False)
    embed.add_field(name='Motivazione', value='Numero massimo di warnings raggiunti', inline=False)
    embed.add_field(name='Warnings Utente', value=str(Saves.get_user_warn(member.id)), inline=False)
    embed.add_field(name='Consentiti Dal Server', value=str(Config.get_kick_after_warns()), inline=False)
    embed.add_field(name='Data Comando', value=get_date(), inline=False)

    return embed


# can't remove warning
def cant_remove_warning_embed(ctx, member):
    embed = discord.Embed(title='Tentativo Rimozione Warning',
                          description='Uno staffer ha tentato di rimuovere un warning ad un utente',
                          color=discord.Color.dark_purple())

    embed.set_thumbnail(url=ctx.author.avatar_url)

    embed.add_field(name='Staffer', value=str(ctx.author), inline=False)
    embed.add_field(name='Utente', value=str(member), inline=False)
    embed.add_field(name='Motivazione', value="L'utente non ha warnings", inline=False)
    embed.add_field(name='Data Comando', value=get_date(), inline=False)

    return embed


# return the embed when a staffer remove a warning from a user
def rm_warning_embed(ctx, member):
    embed = discord.Embed(title='Warning Rimosso',
                          description='uno staffer ha rimosso un warning da un utente',
                          color=discord.Color.dark_purple())

    embed.set_thumbnail(url=ctx.author.avatar_url)

    embed.add_field(name='Staffer', value=str(ctx.author), inline=False)
    embed.add_field(name='Utente', value=str(member), inline=False)
    embed.add_field(name='Data Comando', value=get_date(), inline=False)

    return embed


# return the embed that contain the warned users list
def warned_users_embed(ctx):
    warned_users = Saves.get_warned_users()

    embed = discord.Embed(title='Lista Utenti Warnati',
                          description='lista completa degli utenti warnati nel server',
                          color=discord.Color.dark_purple())

    embed.set_thumbnail(url=ctx.author.avatar_url)

    # if the list is empty
    if not len(warned_users):
        embed.add_field(name='Lista', value='Vuota', inline=False)
        return embed

    i = 0
    for user in warned_users:
        embed.add_field(name=f'# {i + 1}', value=f'Id {user[0]}', inline=False)
        i += 1

    embed.set_footer(text=f"Utilizza il comando {Config.get_prefix()}warnof 'id' oppure '@menzione' per scoprire il "
                          f"numero di warnings di quell'utente")

    return embed


# check if the given role is excluded from the control on the black words
def check_role(message):
    roles_out_blacklist = Config.get_roles_out_blacklist()

    if not len(roles_out_blacklist):
        return False

    for role in message.author.roles:
        if role.id in Config.get_roles_out_blacklist():
            return True

    return False


# check if the channel where the message has been written is a moderation channel
def is_moderation_channel(channel_id):
    moderation_channels = Config.get_moderation_channels()

    if not len(moderation_channels):
        return True

    for id_ in Config.get_moderation_channels():
        if id_ == channel_id:
            return True

    return False


# calculate the amount of time to sleep in the mute command
def calculate_sleep_time(unit, time):
    if unit == 's':
        return 1 * time

    elif unit == 'm':
        return 60 * time

    elif unit == 'h':
        return 3600 * time

    # day
    else:
        return 86400 * time
