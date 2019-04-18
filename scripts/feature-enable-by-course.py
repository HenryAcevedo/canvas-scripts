#
# Henry Acevedo
#
# Purpose: To flip a feature on for a set of courses.
# We are turning on new gradebook at the end of term. As people work on Summer and Fall courses.
# I opted in to new gradebook for the courses to minimize transition issues.

import json
import requests
from canvasapi import Canvas
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')
MYURL = config.get('instance', 'test')
MYTOKEN = config.get('auth', 'token')
canvas = Canvas(MYURL, MYTOKEN)

# Specify which terms we want to ugrab courses in
terms = [37, 38, 39, 40, 41, 42, 43, 44, 45]


def main():
    # this is the account where academic courses are held
    root = canvas.get_account(10)

    # Cycle through the terms listed
    for term in terms:
        courses = root.get_courses(enrollment_term_id=term)
        for course in courses:
            # Form request to turn new gradebook on
            header = {'Authorization': f"Bearer {MYTOKEN}"}
            payload = {'state': 'on'}
            # Send request and receive result
            result = requests.put(f"{MYURL}/api/v1/courses/{course.id}/features/flags/new_gradebook", headers=header, params=payload)
            theJSON = json.loads(result.text)
            print(course)


if __name__ == "__main__":
    main()
