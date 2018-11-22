#!/usr/bin/python
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
    all_chars = string.digits + string.ascii_lowercase + string.ascii_uppercase + string.punctuation
    passwd = ''
    while len(passwd) != length:
        char = random.choice(all_chars)
        if char not in passwd and char != '\\':
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
                passwd = ''
                all_chars = string.digits + string.ascii_lowercase + string.ascii_uppercase + string.punctuation
    return passwd


if __name__ == '__main__':
    print(gen())
