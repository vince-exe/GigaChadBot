from utils.enums import JsonReader

from errors.errors import read_json_errors


import json


def read_json():
    try:
        with open(JsonReader.FileName, 'r') as file:
            data_ = json.load(file)

        # check if he modified the key "Token"
        return data_
    
    except KeyError:
        return JsonReader.KeyModified
    
    except FileNotFoundError:
        return JsonReader.FileNotFound

    except json.decoder.JSONDecodeError:
        return JsonReader.DecodeError


data = read_json_errors(read_json())
