#
# Henry Acevedo
#
# Purpose: Starting point for Canvas scripts.

from canvasapi import Canvas
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')
MYURL = config.get('instance', 'test')
MYTOKEN = config.get('auth', 'token')
canvas = Canvas(MYURL, MYTOKEN)


def main():
    account = canvas.get_account(1)
    print(account)


if __name__ == "__main__":
    main()
