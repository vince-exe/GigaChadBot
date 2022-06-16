from datetime import date, datetime


class InitErrors:
    """
        Class that contain all the errors, that the program could have
        in the initialization part
    """
    Key_Board_Interrupt = -1
    Value_Error = -2
    Connection_Error = -3
    Invalid_Token = -4
    Reading_Settings_Error = -5


class Colors:
    """
        Class that contain all the properties to color the terminal
    """
    Green = "\033[1m" + "\u001b[32m"
    Magenta = "\033[1m" + "\u001b[35m"
    Red = "\033[1m" + "\u001b[31m"
    Yellow = "\033[1m" + "\u001b[33m"
    Blu = "\033[1m" + "\033[94m"
    Reset = "\033[1m" + "\u001b[0m"


# return the current date + the time
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


# class that return True if the given message contain a word that is present in the list
def find_black_word(black_list, message):
    for black_word in black_list:
        for i in range(len(message)):
            k = 0
            while black_word[k] == message[i] and i < len(message):
                k += 1
                i += 1

                if k == len(black_word):
                    return True

    return False
