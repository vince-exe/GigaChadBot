from utils.enums import JsonReader

import json


def read_settings():
    try:
        with open(JsonReader.FileName, 'r') as file:
            data = json.load(file)

        # check if he modified the key "Token"
        return data['Token']
    
    except KeyError:
        return JsonReader.KeyModified
    
    except FileNotFoundError:
        return JsonReader.FileNotFound

    except json.decoder.JSONDecodeError:
        return JsonReader.DecodeError
