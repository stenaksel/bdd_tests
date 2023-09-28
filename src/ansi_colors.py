from enum import Enum

    # ANSI escapes always start with \x1b , or \e , or \033 .
    # These are all the same thing: they're just various ways
    # of inserting the byte 27 into a string.
    # If you look at an ASCII table, 0x1b is literally called ESC.

class ANSIColor(Enum):
    RESET = '\033[0m'
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    GRAY = '\033[90m'

# # Accessing enum members
# print(ANSIColor.RED)
# print(ANSIColor.RED.value)

# # Iterating over enum members
# for color in ANSIColor:
#     print(color, color.value)
