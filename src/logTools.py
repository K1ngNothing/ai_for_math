from enum import IntEnum


class LogLevel(IntEnum):
    DISABLE = 0
    RELEASE = 1
    DEBUG   = 2


COLOR_CODES = {
    'red': '\033[91m', 
    'green': '\033[92m', 
    'yellow': '\033[93m', 
    'blue': '\033[94m', 
    'magenta': '\033[95m', 
    'cyan': '\033[96m'
}
