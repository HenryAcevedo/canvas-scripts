#
# Henry Acevedo
#
# Purpose: Create sandboxes for anyone in Canvas that is enrolled in any
# course/section as a teacher. Will check to avoid creating sandboxes if one
# already exists for that instructor. This also uses that same population
# to enroll those instructors into a self-paced course we created
#

import csv
import datetime
from tqdm import tqdm
from canvasapi import Canvas
from configparser import ConfigParser

# Read info from config.ini file and use those for auth and URL
config = ConfigParser()
config.read('config.ini')
MYURL = config.get('instance', 'test')
MYTOKEN = config.get('auth', 'token')

canvas = Canvas(MYURL, MYTOKEN)
terms = [1, 4, 29, 37, 38, 39, 40, 41, 42, 43, 44, 45]


def main():
    # Get current time for csv file
    now = datetime.datetime.now()
    strNow = now.strftime('%x %X')

    # Append to csv file information about what was done
    datafile = open('TeacherSandbox.csv', 'a')
    datawriter = csv.writer(datafile, lineterminator='\n')

    # Create two empty sets to populate with the populations of instructors
    # and people with sandboxes
    teacherSet = set()
    sandboxSet = set()

    # Get root account and get a list of all courses, also get the
    # subaccount where sandboxes are created for us. This subaccount
    # is only used for these auto sandboxes.
    account = canvas.get_account(1)
    sandbox = canvas.get_account(150)

    for term in terms:
        courses = account.get_courses(enrollment_term_id=term, enrollment_type=['teacher'], include=['teachers'])
        # For each course in canvas check enrollments. If enrollment exists as a
        # teacher but them into a set depending on what subaccount it belongs to.
        # tqdm is used to provide progress
        for course in tqdm(courses, unit=' courses', desc=f'Term {term} Courses'):
            # This is the check for sandbox subaccount, our instance created
            # this subaccount and it has a Canvas id of 150
            if course.account_id != 150:
                for user in course.teachers:
                    teacherSet.add(user['id'])
            else:
                for user in course.teachers:
                    sandboxSet.add(user['id'])

    # Discard empty users and the Example Teacher, in our instance example
    # teacher has 11 as a Canvas ID, so I remove him
    teacherSet.discard(None)
    teacherSet.discard(11)

    # Create an empty set for the self-enrollment course
    # Populate it with enrollments from that specific course
    # Our institute had this course and canvas id 251
    selfSet = set()
    selfCourse = canvas.get_course(251)
    enrollments = selfCourse.get_users()
    for enrollment in enrollments:
        selfSet.add(enrollment.id)

    # Find the difference between all teachers and teachers with
    # sandboxes in that subaccount. Print out how many will be created.
    finalSet = teacherSet - sandboxSet
    print("Creating {0} additional sandboxes.".format(len(finalSet)))

    # Repeat for each teacher in the set
    for teacher in tqdm(finalSet, unit=' sandboxes', desc='Sandboxes created'):
        # Get user object from the id in the set and make a string with
        # the name the sandbox will have.
        cTeacher = canvas.get_user(teacher)
        cName = "{0} Sandbox".format(cTeacher.name)
        # print("Creating " + cName)

        # Create course with this new name, enroll the teacher into the
        # newly created sandbox. By marking state as active you avoid
        # invitations and emails. Write to log as well.
        newSandbox = sandbox.create_course(
            course={'name': cName, 'course_code': cName}
        )
        newSandbox.enroll_user(cTeacher.id, "TeacherEnrollment",
                               enrollment={"enrollment_state": "active"})
        datawriter.writerow([cTeacher.name, getattr(cTeacher,
                            'login_id', None), "Sandbox", strNow])

    # Folllow same process for self-enrollment course, find difference
    # and repeat for each instructor in that set
    selfEnrollSet = teacherSet - selfSet
    for teacher in tqdm(selfEnrollSet, unit=' enrolls', desc='Enrollments'):
        cTeacher = canvas.get_user(teacher)
        # print("Enrolling {0} into self-paced course".format(cTeacher.name))
        selfCourse.enroll_user(cTeacher.id, "StudentEnrollment",
                               enrollment={"enrollment_state": "active"})
        datawriter.writerow([cTeacher.name,
                            getattr(cTeacher, 'login_id', None),
                            "Self-Paced Enrollment", strNow])


if __name__ == "__main__":
    main()
