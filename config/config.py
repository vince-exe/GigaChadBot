from utils.utils import GeneralErrors, Colors

import json


class JsonErrors:
    FileNotFound = -1
    DecodeError = -2
    KeyModified = -3
    MaxPrefError = -4


def read_config(config_path):
    try:
        with open(config_path, 'r') as file:
            data_ = json.load(file)

        # check if the len of the prefix isn't greater than the prefix len
        if len(str(data_['Prefix'])) > data_['MaxPrefixLen']:
            return JsonErrors.MaxPrefError

        # check if he modified the key "Token"
        return data_

    except KeyError:
        return JsonErrors.KeyModified

    except FileNotFoundError:
        return JsonErrors.FileNotFound

    except json.decoder.JSONDecodeError:
        return JsonErrors.DecodeError

    except ValueError:
        return GeneralErrors.ValueError_


def handle_config_errors(error):
    if error == JsonErrors.FileNotFound:
        print(f"{Colors.Red}\nERROR: {Colors.Reset}Config file not found")
        return False

    elif error == JsonErrors.DecodeError:
        print(f"{Colors.Red}\nERROR: {Colors.Reset}Can't read the config file")
        return False

    elif error == JsonErrors.KeyModified:
        print(f"{Colors.Red}\nERROR: {Colors.Reset}Can't read the config file, it seems that you have modified a key"
              f" in the config file")
        return False

    elif error == JsonErrors.MaxPrefError:
        print(f"{Colors.Red}\nERROR: {Colors.Reset}You overpassed the max len of the prefix")
        return False

    elif error == GeneralErrors.ValueError_:
        print(f"{Colors.Red}\nERROR: {Colors.Reset}Check the config file")
        return False

    return error


data = handle_config_errors(read_config('config/config.json'))
