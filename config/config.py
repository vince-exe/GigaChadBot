from utils.utils import GeneralErrors, Colors

import json


class JsonErrors:
    FileNotFound = -1
    DecodeError = -2
    KeyModified = -3
    MaxPrefError = -4
    MaxLenPrefix = -5
    MaxInfoLenError = -6


class JsonConfigsConstants:
    MaxLenPrefix = 3
    MaxInfoLen = 80


def read_config(config_path):
    try:
        with open(config_path, 'r') as file:
            data_ = json.load(file)

        # check if the max len imposed by the user isn't greater of the max len consented by the program
        if int(data_['MaxPrefixLen']) > JsonConfigsConstants.MaxLenPrefix:
            return JsonErrors.MaxLenPrefix

        # check if the len of the prefix isn't greater than the prefix len
        if len(data_['Prefix']) > data_['MaxPrefixLen']:
            return JsonErrors.MaxPrefError

        # check if the len of the info ban/kick isn't greater of the max len for the info
        if len(data_['InfoBanKick']) > JsonConfigsConstants.MaxInfoLen:
            return JsonErrors.MaxInfoLenError

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
        print(f"{Colors.Red}\nERROR: {Colors.Reset}file di configurazione non trovato")
        return False

    elif error == JsonErrors.MaxLenPrefix:
        print(f"{Colors.Red}\nERROR: {Colors.Reset}il limite massimo della lunghezza del prefisso che hai impostato, "
              f"supera il limite massimo che il programma consente di impostare che equivale a: "
              f"{JsonConfigsConstants.MaxLenPrefix}")
        return False

    elif error == JsonErrors.MaxInfoLenError:
        print(f"{Colors.Red}\nERROR: {Colors.Reset}la lunghezza della info/ban supera quella che il programma consente "
              f"che equivale a: {JsonConfigsConstants.MaxInfoLen}")
        return False

    elif error == JsonErrors.DecodeError:
        print(f"{Colors.Red}\nERROR: {Colors.Reset}impossibile leggere il file di configurazione, controllallo")
        return False

    elif error == JsonErrors.KeyModified:
        print(f"{Colors.Red}\nERROR: {Colors.Reset}hai modificato il nome di una key nel file di configurazione"
              f" in the config file")
        return False

    elif error == JsonErrors.MaxPrefError:
        print(f"{Colors.Red}\nERROR: {Colors.Reset}il tuo prefisso per il bot, è troppo lungo")
        return False

    elif error == GeneralErrors.ValueError_:
        print(f"{Colors.Red}\nERROR: {Colors.Reset}controlla il file di configurazione")
        return False

    return error


data = handle_config_errors(read_config('config/config.json'))
