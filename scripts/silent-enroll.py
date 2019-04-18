#
# Henry Acevedo
#
# Purpose: Enroll without notification in course


from canvasapi import Canvas
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')
MYURL = config.get('instance', 'test')
MYTOKEN = config.get('auth', 'token')
canvas = Canvas(MYURL, MYTOKEN)


def main():
    # Open txt file which contains one user sis_id per line, can also be done with other field
    with open("toEnroll.txt", "r") as myFile:
        # Cycle through each line of the file
        for line in myFile:
            line = line.strip()
            # get the canvas user, by modifying the id_type you can choose what field to search by
            cTeacher = canvas.get_user(line, id_type='sis_login_id')
            # Choose course number to enroll people in
            course = canvas.get_course(32980)
            # Enroll user with TeacherRole, mark enrollment as active so no invitation is sent.
            course.enroll_user(cTeacher.id, "TeacherEnrollment",
                               enrollment={"enrollment_state": "active"})


if __name__ == "__main__":
    main()
