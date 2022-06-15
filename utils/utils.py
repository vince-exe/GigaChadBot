from datetime import date, datetime

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


def get_date():
    year = date.today().year

    month = int(date.today().month)
    tmp_month = month

    if month <= 9:
        month = f'0{tmp_month}'
    else:
        tmp_month = str(month)
        month = tmp_month

    day = int(date.today().day)
    tmp_day = day

    if day <= 9:
        day = f'0{tmp_day}'
    else:
        tmp_day = str(day)
        day = tmp_day

    time = datetime.now()
    current_time = time.strftime("%H:%M:%S")
    return f'{day}/{month}/{year}\t\t{current_time}'


def find_black_word(black_list, message):
    for black_word in black_list:
        for i in range(len(message)):
            k = 0
            while black_word[k] == message[i] and i < len(message) and k < len(black_word):
                k += 1
                i += 1

                if k == len(black_word):
                    return True

    return False
