import os

from utils.enums import JsonReader, GeneralErrors, Colors

import json


def read_json_errors(error):
    if error == JsonReader.FileNotFound:
        print(f"{Colors.Red}\nERROR: {Colors.Reset}Config file not found")
        return False

    elif error == JsonReader.DecodeError:
        print(f"{Colors.Red}\nERROR: {Colors.Reset}Can't read the {JsonReader.FileName} file")
        return False

    elif error == JsonReader.KeyModified:
        print(f"{Colors.Red}\nERROR: {Colors.Reset}Can't read the config file, it seems that you have modified a key"
              f" in the config file")
        return False

    elif error == JsonReader.MaxPrefError:
        print(f"{Colors.Red}\nERROR: {Colors.Reset}You overpassed the max len of the prefix")
        return False

    elif error == GeneralErrors.ValueError_:
        print(f"{Colors.Red}\nERROR: {Colors.Reset}Check the config file")
        return False

    return error


def read_json():
    try:
        with open(JsonReader.FileName, 'r') as file:
            data_ = json.load(file)

        # check if the len of the prefix isn't greater than the prefix len
        if len(str(data_['Prefix'])) > data_['MaxPrefixLen']:
            return JsonReader.MaxPrefError

        # check if he modified the key "Token"
        return data_

    except KeyError:
        return JsonReader.KeyModified
    
    except FileNotFoundError:
        return JsonReader.FileNotFound

    except json.decoder.JSONDecodeError:
        return JsonReader.DecodeError

    except ValueError:
        return GeneralErrors.ValueError_


def load_ext(dir_name, bot):
    for filename in os.listdir(f'./{dir_name}'):
        if filename.endswith('.py'):
            bot.load_extension(f'{dir_name.replace("/", ".")}.{filename[:-3]}')


data = read_json_errors(read_json())
