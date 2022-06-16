from utils.utils import Colors

import json


class JsonErrors:
    """
        This class has all the json errors
        used in this program
    """
    File_Not_Found_Error = -1
    Decode_File_Error = -2
    Key_Modified_Error = -3
    Max_Prefix_Error = -4
    Max_Len_Prefix_Error = -5
    Max_Info_Len_Error = -6


class Config:
    """
        This class takes care of reading the json configuration file and
        is responsible for providing methods to access the configuration properties
    """
    __configs = None
    __error = None

    # this dictionary has all the names of the default config.json keys
    default_keys = {
        'Token': None,
        'MaxPrefixLen': None,
        'Prefix': None,
        'LogChannel': None,
        'FailLogChannel': None,
        'SpamLogChannel': None,
        'InfoBanKick': None
    }

    # class constants
    Max_Len_Prefix = 3
    Max_Info_Len = 80

    # load the config.json file
    @classmethod
    def load_configs(cls, path):
        try:
            with open(path, 'r') as file:
                Config.__configs = json.load(file)

        except FileNotFoundError:
            Config.__error = f'\n{Colors.Red}ERROR: {Colors.Reset}non ho trovato il config file'
            Config.__configs = None

        except json.decoder.JSONDecodeError:
            Config.__error = f'\n{Colors.Red}ERROR: {Colors.Reset}impossibile leggere il config file'
            Config.__configs = None

    # this method return True if the keys name are correct
    @classmethod
    def check_keys(cls):
        return set(Config.default_keys.keys()) == set(Config.__configs.keys())

    @classmethod
    def get_token(cls):
        return str(Config.__configs['Token'])

    @classmethod
    def get_max_prefix_len(cls):
        return str(Config.__configs['MaxPrefixLen'])

    @classmethod
    def get_prefix(cls):
        return str(Config.__configs['Prefix'])

    @classmethod
    def get_log_channel(cls):
        return str(Config.__configs['LogChannel'])

    @classmethod
    def get_fail_log_channel(cls):
        return str(Config.__configs['FailLogChannel'])

    @classmethod
    def get_spam_log_channel(cls):
        return str(Config.__configs['SpamLogChannel'])

    @classmethod
    def get_info_ban_kick(cls):
        return str(Config.__configs['InfoBanKick'])

    # main method, used to [inizialize] the class
    @classmethod
    def init(cls):
        # check if the class failed to load the json file
        if Config.__configs is None:
            print(Config.__error)
            return False

        # check if the keys aren't equals
        elif not Config.check_keys():
            print(f"{Colors.Red}\nERROR: {Colors.Reset}hai modificato il nome di una key nel file di configurazione")
            Config.__configs = None
            return False

        # check if the max len imposed by the user isn't greater of the max len consented by the software
        elif int(Config.get_max_prefix_len()) > Config.Max_Len_Prefix:
            print(
                f"{Colors.Red}\nERROR: {Colors.Reset}il limite massimo della lunghezza del prefisso che hai impostato, "
                f"supera il limite massimo che il programma consente di impostare che equivale a: "
                f"{Config.Max_Len_Prefix}"
                )
            return False

        # check if the len of the prefix isn't grater then the len of max len prefix
        elif len(Config.get_prefix()) > len(Config.get_max_prefix_len()):
            print(f"{Colors.Red}\nERROR: {Colors.Reset}il tuo prefisso per il bot, è troppo lungo")
            return False

        # check if the len of the info ban/kick isn't greater of the max len for the info
        elif len(Config.get_info_ban_kick()) > Config.Max_Info_Len:
            print(
                f"{Colors.Red}\nERROR: {Colors.Reset}la lunghezza della info/ban supera quella che il programma consente"
                f"che equivale a: {Config.Max_Info_Len}")
            return False

        # the json file passed all the cases
        return True


# load the config file
Config.load_configs('json_files/config.json')
