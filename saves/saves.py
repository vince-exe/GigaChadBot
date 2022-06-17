from utils.utils import Colors

import json


class Saves:
    """
        This class takes care of saving in specific json files,
        all the data that the bot has accumulated during execution
    """
    __black_words_json = None
    __black_words_list = []
    __new_black_words_saves = False
    __blackwords_json_path = None

    # variable that contain the possible error in reading the json file
    __errors = None


    @classmethod
    def load_black_words_list(cls, path):
        Saves.__blackwords_json_path = path
        try:
            with open(path, 'r') as file:
                Saves.__black_words_json = json.load(file)

        except FileNotFoundError:
            Saves.__errors = f'\n{Colors.Red}ERROR: {Colors.Reset}non ho trovato il file contenente le black words'
            Saves.__black_words_json = None

        except json.decoder.JSONDecodeError:
            Saves.__errors = f'\n{Colors.Red}ERROR: {Colors.Reset}impossibile leggere il file contenente le black words'
            Saves.__black_words_json = None

    # return the black_words_list
    @classmethod
    def get_blackwords(cls):
        return Saves.__black_words_list

    # add a black_word to the black words list
    @classmethod
    def add_black_word(cls, black_word):
        # if the black_word already is in the black_words_list
        if black_word in Saves.__black_words_list:
            return False

        Saves.__black_words_list.append(black_word)
        Saves.__new_black_words_saves = True
        return True

    # saves all the new modify to the json files
    @classmethod
    def save_all(cls):
        # check if the class has to save new things
        if Saves.__new_black_words_saves:
            Saves.__black_words_json['BlackWords'] = Saves.__black_words_list

            with open(Saves.__blackwords_json_path, 'w') as file:
                json.dump(Saves.__black_words_json, file)

    # main method to initialize the class
    @classmethod
    def init(cls):
        if Saves.__black_words_json is None:
            print(Saves.__errors)
            return False

        # save the blackwords list in this list
        Saves.__black_words_list = Saves.__black_words_json['BlackWords']
        return True


# load the black_words json file
Saves.load_black_words_list('json_files/black_words.json')
