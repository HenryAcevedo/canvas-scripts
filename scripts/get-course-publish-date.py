#
# Henry Acevedo
#
# Purpose: Get date when a range of courses were published
#

import csv
import json
import requests
from tqdm import tqdm
from canvasapi import Canvas
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')
MYURL = config.get('instance', 'test')
MYTOKEN = config.get('auth', 'token')
canvas = Canvas(MYURL, MYTOKEN)


def main():
    # Academic subaccount
    account = canvas.get_account(10)

    # Create a csv for the term, write header row
    with open('CanvasPublishDatesS19.csv', 'w') as csvFile:
        csvWriter = csv.writer(csvFile, lineterminator='\n')
        csvWriter.writerow(['account', 'Parent', 'Course', 'When'])

        # Get courses that were published in current 29. Change term id for your institution
        courses = account.get_courses(
            with_enrollments=True,
            published=True,
            enrollment_term_id=29)

        # Cycle through each course in our results
        for course in tqdm(courses):
            # Build request and send
            url = MYURL + f'/api/v1/audit/course/courses/{course.id}'
            BearToken = 'Bearer {}'.format(MYTOKEN)
            header = {'Authorization': BearToken}
            r = requests.get(url, headers=header)
            # print(r.status_code)

            # If request is fine, process and log into csv file
            if r.status_code == 200:
                logs = json.loads(r.text)

                for log in logs['events']:
                    if log['event_type'] == 'published':
                        # print(log['created_at'])
                        csvWriter.writerow([
                            account.name,
                            course.account_id,
                            course.id,
                            log['created_at']])


if __name__ == "__main__":
    main()
