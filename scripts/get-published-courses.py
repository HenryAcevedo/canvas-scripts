#
# Henry Acevedo
#
# Purpose: Log courses that are published and not for data visualization purposes.
#

import csv
from canvasapi import Canvas
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')
MYURL = config.get('instance', 'test')
MYTOKEN = config.get('auth', 'token')

canvas = Canvas(MYURL, MYTOKEN)

# Specify information for term and filename

# Fall 18
# fn = 'SubaccountsPublish.csv'
# term_id = 27

# Winter 19
# fn = '2191SubaccountsPublish.csv'
# term_id = 28

# Spring 19
fn = '2193SubaccountsPublish.csv'
term_id = 29


def main():
    # Academic courses subaccount
    root = canvas.get_account(10)
    accounts = root.get_subaccounts()

    # Create a .csv with filename from above and write heare
    with open(fn, 'w') as csvFile:
        csvWriter = csv.writer(csvFile, lineterminator='\n')
        csvWriter.writerow(['account', 'Parent', 'Course', 'Status'])

        # Cycle through subaccounts in this account
        for account in accounts:
            # Get courses in term with a teacher, and include number of students in course
            courses = account.get_courses(
                enrollment_type=['teacher'],
                enrollment_term_id=term_id,
                include=['total_students'])

            # Cycle through courses
            for course in courses:
                # If no students ignore, otherwise log in csv as published or unpublished
                if course.total_students != 0:
                    if course.workflow_state == 'unpublished':
                        csvWriter.writerow([
                            account.name,
                            course.account_id,
                            course.id, 'Unpublished'])
                    else:
                        csvWriter.writerow([
                            account.name,
                            course.account_id,
                            course.id, 'Published'])


if __name__ == "__main__":
    main()
