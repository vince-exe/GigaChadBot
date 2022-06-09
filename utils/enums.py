class JsonReader:
    FileName = 'config.json'
    FileNotFound = -1
    DecodeError = -2
    KeyModified = -3
    MaxPrefError = -4


class GeneralErrors:
    ReadingSettingsError = -5
    KeyBoardInterrupt_ = -1
    ValueError_ = -2


class DiscordErrors:
    InvalidToken = -1


class Colors:
    Green = "\033[1m" + "\u001b[32m"
    Magenta = "\033[1m" + "\u001b[35m"
    Red = "\033[1m" + "\u001b[31m"
    Yellow = "\033[1m" + "\u001b[33m"
    Blu = "\033[1m" + "\033[94m"
    Reset = "\033[1m" + "\u001b[0m"
