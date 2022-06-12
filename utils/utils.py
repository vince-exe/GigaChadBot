import os

from utils.enums import JsonReader, GeneralErrors

from errors.errors import read_json_errors


import json


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
