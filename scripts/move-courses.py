#
# Henry Acevedo
#
# Purpose: Update courses from one account to another.
#

# import csv
from canvasapi import Canvas
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')
MYURL = config.get('instance', 'TEST')
MYTOKEN = config.get('auth', 'token')

canvas = Canvas(MYURL, MYTOKEN)


def main():
	# Grab account identified as 2 and get those courses
	account = canvas.get_account(2)
	courses = account.get_courses()

	# For each course in account above, modify account to subaccount 14
	for course in courses:
		course.update(course={'account_id': 14})
		print(course)


if __name__ == "__main__":
	main()
