# Sample project for Canvas hub course
This sample project could be helpful in seeing how our team has managed the hub course. It isn't a project that will run, but these pieces can help do specific tasks like connecting to the database or seeing Python code for checking a Canvas score.

# Canvasapi
The University of Central Florida has created a Canvas API wrapper that is a good resource to begin using the Canvas API. You can find more information about it on their [canvasapi Github Page](https://github.com/ucfopen/canvasapi) they also provide [documentation](https://canvasapi.readthedocs.io/en/latest/). To install this package, you can run `pip install canvasapi`.


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

# Resource Sites

* [UCF canvasapi Documentation](https://canvasapi.readthedocs.io/en/latest/)
* [Canvas API Documentation](https://canvas.instructure.com/doc/api/file.object_ids.html)
* [Canvas Live API](https://calstatela.instructure.com/doc/api/live)
* [Canvas Unsupported Scripts](https://github.com/unsupported/canvas)
You can find unsupported scripts for Canvas here. For example they have a script for batch restoring backup files from other LMS into Canvas.
* [Canvas API Basics](https://community.canvaslms.com/docs/DOC-14390-canvas-apis-getting-started-the-practical-ins-and-outs-gotchas-tips-and-tricks)
* [Security around Developer Keys](https://community.canvaslms.com/groups/admins/blog/2019/01/24/administrative-guidelines-for-managing-inherited-developer-keys#comments)
