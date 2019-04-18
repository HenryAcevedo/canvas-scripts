#
# Henry Acevedo
#
# Purpose: Modifying external tools for things like disabling from course navigation by default
#

from canvasapi import Canvas
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')
MYURL = config.get('instance', 'test')
MYTOKEN = config.get('auth', 'token')
canvas = Canvas(MYURL, MYTOKEN)


def main():
    # This will give you a list of tool names and id.
    # After you know the id you can uncomment other lines to modify the tool.
    account = canvas.get_account(1)
    exTools = account.get_external_tools()

    for tool in exTools:
        print(tool)

    # tool = account.get_external_tool(55)
    # print(tool)
    # tool.edit(course_navigation={'default': 'disabled})
    # tool.edit(assignment_selection={'enabled': False})
    # tool.edit(not_selectable=True)


if __name__ == "__main__":
    main()
