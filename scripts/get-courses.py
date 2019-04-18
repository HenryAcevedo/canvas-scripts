#
# Henry Acevedo
#
# Purpose: Print a list of canvas courses

from canvasapi import Canvas
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')
MYURL = config.get('instance', 'test')
MYTOKEN = config.get('auth', 'token')
canvas = Canvas(MYURL, MYTOKEN)


def main():
    account = canvas.get_account(1)
    courses = account.get_courses()

    for course in courses:
        print(course)


if __name__ == "__main__":
    main()
