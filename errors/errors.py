from utils.enums import *


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
