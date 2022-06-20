from utils.utils import Colors

import json


class Saves:
    """
        This class takes care of saving in specific json files,
        all the data that the bot has accumulated during execution
    """
    __black_words_json = None
    __black_words_list = []
    __black_list_saves = False
    __blackwords_json_path = None

    __citations_json = None
    __citations_json_path = None
    __citations_list = []
    __citations_saves = False

    # variable that contain the possible error in reading the json file
    __errors = None

    # check if there are any changes
    @classmethod
    def check_saves(cls):
        if Saves.__citations_saves or Saves.__black_list_saves:
            return True

        return False

    # check if there is any error
    @classmethod
    def check_json_errors(cls):
        if Saves.__black_words_json is None:
            return False

        elif Saves.__citations_json is None:
            return False

        return True

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

    @classmethod
    def load_citations(cls, path):
        Saves.__citations_json_path = path
        try:
            with open(path, 'r') as file:
                Saves.__citations_json = json.load(file)

        except FileNotFoundError:
            Saves.__errors = f'\n{Colors.Red}ERROR: {Colors.Reset}non ho trovato il file contenente le citazioni'
            Saves.__citations_json = None

        except json.decoder.JSONDecodeError:
            Saves.__errors = f'\n{Colors.Red}ERROR: {Colors.Reset}impossibile leggere il file contenente le citazioni'
            Saves.__citations_json = None

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
        Saves.__black_list_saves = True
        return True

    # remove the given black word from the black words list
    @classmethod
    def rm_black_word(cls, black_word):
        # try to remove the black word if it's present in the list, else return False
        try:
            Saves.__black_words_list.remove(black_word)
            Saves.__black_list_saves = True
            return True
        except ValueError:
            return False

    # return the list of citations
    @classmethod
    def get_citations(cls):
        return Saves.__citations_list

    # saves all the new modify to the json files
    @classmethod
    def save_all(cls):
        # check if the class has to save new things
        if Saves.check_saves():
            # if there are new modify in the black words list, save it
            if Saves.__black_list_saves:
                Saves.__black_words_json['BlackWords'] = Saves.__black_words_list

                # open the json file and rewrite the Black Words list, then close the file
                with open(Saves.__blackwords_json_path, 'w') as file:
                    json.dump(Saves.__black_words_json, file)

            if Saves.__citations_saves:
                pass

    # main method to initialize the class
    @classmethod
    def init(cls):
        if not Saves.check_json_errors():
            print(Saves.__errors)
            return False

        # save the blackwords list in this list
        Saves.__black_words_list = Saves.__black_words_json['BlackWords']
        # save the citations in the citations list
        Saves.__citations_list = Saves.__citations_json['Citations']

        return True


# load the black_words json file
Saves.load_black_words_list('json_files/black_words.json')
# load the citations json file
Saves.load_citations('json_files/citations.json')

