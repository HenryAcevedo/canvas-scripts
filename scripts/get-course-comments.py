#
# Henry Acevedo
#
# Purpose: Get Comments from assignments for a course


import csv
from canvasapi import Canvas
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')
MYURL = config.get('instance', 'test')
MYTOKEN = config.get('auth', 'token')
canvas = Canvas(MYURL, MYTOKEN)


def main():
    # Will begin by asking for a course id, can be found in URL of course
    # Will then grab that course and get a list of assignments
    num = int(input('Enter your course number: '))
    course = canvas.get_course(num)
    assignments = course.get_assignments()

    # Create a .csv file to populate with our findings, write header
    with open("SubComments.csv", "w", newline='') as myFile:
        writer = csv.writer(myFile)
        writer.writerow(['Assignment Name', 'Preview Submission', 'Submission Author', 'Comment', 'Comment Author'])

        # Cycle through the assignments in the course
        for assignment in assignments:
            # get the submissions for the current assignment
            submissions = assignment.get_submissions(include=['submission_comments', 'user'])

            # For each submision
            for sub in submissions:
                # For each comment in current submission
                for comment in sub.submission_comments:
                    # Print and write to .csv file
                    print(assignment.name, sub.preview_url, sub.user['name'], comment['comment'], comment['author_name'])
                    writer.writerow([assignment.name, sub.preview_url, sub.user['name'], comment['comment'], comment['author_name']])


if __name__ == "__main__":
    main()
