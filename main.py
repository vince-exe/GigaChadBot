from errors.errors import *

from utils.utils import read_settings
from utils.enums import GeneralErrors


if __name__ == '__main__':
    token = read_settings_errors(read_settings())
    
    if not token:
        exit(GeneralErrors.ReadingSettingsError)
        
    print(token)
