#
# Henry Acevedo
#
# Purpose: Print a list of Canvas users
from canvasapi import Canvas
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')
MYURL = config.get('instance', 'test')
MYTOKEN = config.get('auth', 'token')
canvas = Canvas(MYURL, MYTOKEN)


def main():
    account = canvas.get_account(1)
    users = account.get_users()

    for user in users:
        print(user)


if __name__ == "__main__":
    main()
