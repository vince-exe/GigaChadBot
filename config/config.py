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
        'Prefix': None,
        'LogChannel': None,
        'FailLogChannel': None,
        'SpamLogChannel': None,
        'InfoBanKick': None,
        'RolesOutBlackWordCheck': None,
        'MaxMessageLen': None,
        'ModerationChannels': None,
        'InteractionChannels': None,
        'MuteRole': None,
        'KickAfterWarns': None
    }

    # this dictionary contains all the commands name and their descriptions
    commands_list = {
        'hello': "il bot saluterà chi invoca questo comando",
        'repeat': "il bot ripeterà la frase dettata",
        'whois': "ritorna le informazioni sull'utente taggato dopo il comando",
        'chinfo': "ritorna le informazioni di uno specifico canale",
        'blackwords': "manda nei DM la lista delle parole bandite all'utente che ha eseguito il comando",
        'citations': "manda nei DM la lista delle citazioni del bot all'utente che ha eseguito il comando",
        'citation': "il bot annuncia una citazione casuale nel canale in cui il comando è stato eseguito",
        'kick': "espelle un utente dal server",
        'ban': "banna un utente dal server",
        'set_blacklist': "attiva o disattiva il controllo del bot sulle blackwords, di default è attivo",
        'get_blacklist': "ritorna lo stato della blacklist (attivo / disattivo)",
        'add_blackword': "aggiunge una blackword all'elenco di blackwords",
        'rm_blackword': "rimuove una blackword dall'elenco di blackwords",
        'clear_': "rimuove un numero dato di messaggi dal canale in cui il comando è stato evocato",
        'clear': "rimuove tutti i messaggi nel canale in cui il comando è stato evocato",
        'mute': "muta (testualmente) un utente per un certo periodo di tempo dato",
        'unmute': "smuta (testualmente) un utente",
        'unban': "sbanna un utente",
        'banlist': "manda la lista completa degli utenti bannati nel canale in cui il comando è stato evocato",
        'random': "genera un numero casuale tra i due numeri che gli vengono passati",
        'hot': "simulazione del gioco testa o croce",
        'warn': "avvisa un utente per un suo comportamento, dopo un tot numeri di worn l'utente verrà sanzionato",
        'pic': "ritorna la pic di un utente taggato",
        'warnof': "ritorna il numero di warn di uno specifico utente taggato",
        'warned_users': "ritorna la lista degli utenti warnati nel server"
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
    def get_prefix(cls):
        return str(Config.__configs['Prefix'])

    @classmethod
    def get_log_channel(cls):
        return Config.__configs['LogChannel']

    @classmethod
    def get_fail_log_channel(cls):
        return Config.__configs['FailLogChannel']

    @classmethod
    def get_spam_log_channel(cls):
        return Config.__configs['SpamLogChannel']

    @classmethod
    def get_info_ban_kick(cls):
        return str(Config.__configs['InfoBanKick'])

    @classmethod
    def get_roles_out_blacklist(cls):
        return Config.__configs['RolesOutBlackWordCheck']

    @classmethod
    def get_max_message_len(cls):
        return Config.__configs['MaxMessageLen']

    @classmethod
    def get_moderation_channels(cls):
        return Config.__configs['ModerationChannels']

    @classmethod
    def get_interaction_channels(cls):
        return Config.__configs['InteractionChannels']

    @classmethod
    def get_mute_role(cls):
        return Config.__configs['MuteRole']

    @classmethod
    def get_kick_after_warns(cls):
        return Config.__configs['KickAfterWarns']

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

        # check if the len of the prefix isn't grater than 3
        elif len(Config.get_prefix()) > Config.Max_Len_Prefix:
            print(f"{Colors.Red}\nERROR: {Colors.Reset}il tuo prefisso per il bot, è troppo lungo")
            return False

        # check if the len of the info ban/kick isn't greater of the max len for the info
        elif len(Config.get_info_ban_kick()) > Config.Max_Info_Len:
            print(
                f"{Colors.Red}\nERROR: {Colors.Reset}la lunghezza della info/ban supera quella che il programma consente"
                f"che equivale a: {Config.Max_Info_Len}")
            return False

        # check the option KickAfterWarns
        elif Config.get_kick_after_warns() <= 0:
            print(f"{Colors.Red}\nERROR: {Colors.Reset}non puoi settare un numero uguale o minore di zero nell'opzione"
                  f" 'KickAfterWarns'")
            return False

        # the json file passed all the cases
        return True


# load the config file
Config.load_configs('json_files/config.json')
