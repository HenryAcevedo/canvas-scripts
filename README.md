# canvas-scripts
Collection of scripts that help automate tasks and find information.

# Setup
First thing you will need is Python version 3.6 or higher. You can check if you have Python by running `python --version`. To begin downloading and installing Python [start here](https://wiki.python.org/moin/BeginnersGuide/Download).

Some operating systems may install Python 2.7 as the default Python client; sometimes this means running `python3 --version` to differentiate between the pre-installed and the new one. After you can run the `python --version` command and see something higher than 3.6 we can continue with the next package.

The University of Central Florida has created a Canvas API wrapper that is a good resource to begin using the Canvas API. You can find more information about it on their [canvasapi Github Page](https://github.com/ucfopen/canvasapi) they also provide [documentation](https://canvasapi.readthedocs.io/en/latest/). To install this package, you can run `pip install canvasapi` from an admin command prompt. If your operating system has Python 2.7 as the default, you can try running `pip3 install canvaspi`.

Our next step is to configure the scripts to use your Canvas instance. Open the config.ini file in the scripts folder. Modify the URLs to match your Canvas instance. You will also need to create an Access Token in Canvas and place that in the config.ini. Use these steps on generating an [Access Token](https://community.canvaslms.com/docs/DOC-10806-4214724194). Make sure to remove the braces as well.

Now we will try to run our first script. The only thing that the template script does is get the main subaccount and print it. To run it make sure your command prompt or terminal is in the scripts folder and run `python template.py` or `python3 template.py`.

If you see the name of your account printed out, Congratulations! If not there is something that may need to troubleshoot. Make sure you did not miss a step above.

# Using config.ini
The reason I like using the config.ini is the ease of switching between production, test, and beta. If needed I can also delete my access token and replace it easily without having to change the token in every script that I have. In the Python file, you should have a couple of lines
```python
config = ConfigParser()
config.read('config.ini')
MYURL = config.get('instance', 'test')
MYTOKEN = config.get('auth', 'token')
canvas = Canvas(MYURL, MYTOKEN)
```
These lines read from the config.ini file and select the instance. By changing the instance from test to prod or beta, you can change which instance the code will run in. I suggest running things in beta or test first, then running in prod when you see the desired result.

# Resources

## Sites
* [UCF canvasapi Documentation](https://canvasapi.readthedocs.io/en/latest/)
* [Canvas API Documentation](https://canvas.instructure.com/doc/api/file.object_ids.html)
* [Canvas Live API](https://calstatela.instructure.com/doc/api/live)
* [Canvas Unsupported Scripts](https://github.com/unsupported/canvas)
You can find unsupported scripts for Canvas here. For example they have a script for batch restoring backup files from other LMS into Canvas.
* [Canvas API Basics](https://community.canvaslms.com/docs/DOC-14390-canvas-apis-getting-started-the-practical-ins-and-outs-gotchas-tips-and-tricks)
* [Security around Developer Keys](https://community.canvaslms.com/groups/admins/blog/2019/01/24/administrative-guidelines-for-managing-inherited-developer-keys#comments)


## Additional packages
You can install these using the pip command from earlier.
* [Requests](http://docs.python-requests.org/en/master/)
You will probably need this if you ever encounter something that you want that is not supported by canvasapi
* [tqdm](https://github.com/tqdm/tqdm)
I use this sometimes when I want to a see a progress bar in a script

## Text Editors
* [Notepad++](https://notepad-plus-plus.org/)
* [Sublime](https://www.sublimetext.com/)
* [Visual Studio Code](https://code.visualstudio.com/)
    * [Python Extension for VSCode](https://marketplace.visualstudio.com/itemdetails?itemName=ms-python.python)
* [Atom](https://atom.io/)
* [Mu](https://codewith.mu/)

## Version Control
* [git](https://git-scm.com/)
If you find yourself making frequent changes or working on longer scripts, I highly suggest using a version control so that you don't accidentally delete things and are unable to recover them.