__author__ = 'user'

import random
from ctypes import *


class JustTest:
    def __init__(self, amt):
        self.__amt = amt

    def get_amt(self):
        return self.__amt

    def add_amt(self, amt):
        self.__amt += amt


def say(words):
    """
    print words to consel
    """
    aaa = words
    msvcrt = cdll.msvcrt
    msvcrt.printf(words)


class Barley(Structure):
    _fields_ = [
        ("age", c_int),
        ("name", c_char * 10)
    ]

if __name__ == "__main__":
    aa = "123"
    bb = aa.rjust(7, '0')
    print bb