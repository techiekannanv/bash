"""This is just simple password generator using random module.
This will create 8 char password with combination of alpha,
numeric and special character. The below condition should met
1 - lower case
1 - upper case
1 - numeric
1 - special character
"""

from __future__ import print_function
import string
import random

def gen(length=8):
    chars = dict(special=0, lower=0, upper=0, numeric=0)
    all_chars = string.printable.replace(string.whitespace, '')
    passwd = ''
    tried = 1
    while len(passwd) != length:
        char = random.choice(all_chars)
        if char not in passwd:
            if char in string.punctuation:
                chars['special'] = 1
            elif char in string.ascii_lowercase:
                chars['lower'] = 1
            elif char in string.ascii_uppercase:
                chars['upper'] = 1
            elif char in string.digits:
                chars['numeric'] = 1
            passwd += char
            all_chars = all_chars.replace(char, '')
            if len(passwd) == length and list(chars.values()) != [1, 1, 1, 1]:
                tried += 1
                passwd = ''
                all_chars = string.printable.replace(string.whitespace, '')
    # print('DEBUG: Total tried ',tried,' times')
    return passwd


if __name__ == '__main__':
    print(gen())
