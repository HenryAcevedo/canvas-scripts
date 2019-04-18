#
# Henry Acevedo
#
# Purpose: Create module with text header and link to survey


from canvasapi import Canvas
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')
MYURL = config.get('instance', 'test')
MYTOKEN = config.get('auth', 'token')
canvas = Canvas(MYURL, MYTOKEN)


def main():
    # Open a txt file which contains one course id per line and cycle through each line
    with open('hybrid-courses.txt', 'r') as cFile:
        for line in cFile:
            # Get the course that corresponds to current line
            course_id = int(line)
            course = canvas.get_course(course_id)

            # Create a module and put it at the top
            module = course.create_module(
                module={
                    'name': 'Hybrid Course - Student Survey',
                    'position': 1})

            # Create a header
            header = module.create_module_item(
                module_item={
                    'title': 'Your voice counts! Share your feedback on your hybrid learning experience.',
                    'type': 'SubHeader',
                    'content_id': ''})

            # Create a URL that opens externally, modify the URL with dynamic content passing to survey as parameter
            url = f'https://url.co1.qualtrics.com/jfe/form/xxxxxxxxxx?Source={course_id}'
            link = module.create_module_item(
                module_item={
                    'title': 'Fall 2018 - Hybrid Course - Student Survey Links to an external site.',
                    'type': 'ExternalUrl',
                    'content_id': '',
                    'external_url': url,
                    'new_tab': True})

            # Publish the items
            module.edit(module={'published': True})
            header.edit(module_item={'published': True})
            link.edit(module_item={'published': True})

if __name__ == "__main__":
    main()
