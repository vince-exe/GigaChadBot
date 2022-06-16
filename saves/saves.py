from utils.utils import Colors

import json


class Saves:
    """
        This class takes care of saving in specific json files,
        all the data that the bot has accumulated during execution
    """
    black_words_json = None

    @classmethod
    def load_black_words_list(cls, path):
        try:
            with open(path, 'r') as file:
                Saves.black_words_json = json.load(file)

        except FileNotFoundError:
            print(f'\n{Colors.Red}ERROR: {Colors.Reset}non ho trovato il file contenente le black words')
            Saves.black_words_json = None

        except json.decoder.JSONDecodeError:
            print(f'\n{Colors.Red}ERROR: {Colors.Reset}impossibile leggere il file contenente le black words')
            Saves.black_words_json = None


# load the black_words json file
Saves.load_black_words_list('json_files/black_words.json')
