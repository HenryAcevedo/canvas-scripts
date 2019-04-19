#
# Henry Acevedo
#
# Purpose: This script is used for monitoring and reporting on the SIS sync process.
# It monitors that the sync process hasn't stopped for an extended duration. It also reports
# when there are unexpected results like an error message or when there are less than 6 files
# which is what is sent every time. It also downloads the sent files for record keeping on an
# encrypted partition.
#
# If not using Windows/Outlook you may need to remove or reconfigure email portion of code.
#

import requests
import json
import os
import shutil
import pytz
from datetime import datetime, timedelta
from configparser import ConfigParser
import win32com.client as win32


config = ConfigParser()
config.read('config.ini')
MYURL = config.get('instance', 'PROD')
MYTOKEN = config.get('auth', 'token')
MYTOKEN = 'Bearer {}'.format(MYTOKEN)
TOTAL = 0


def sendEmail(import_id):
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = 'email.address.edu'
    mail.Subject = f"Canvas import error in #{import_id}"
    mail.HTMLBody = f"Canvas import error in #{import_id}"
    mail.Send()


def sendAlert(msg):
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = 'email@address.edu'
    mail.Subject = msg
    mail.HTMLBody = msg
    mail.Send()


def main():
    # Build request to Canvas SIS import API endpoint, will check requests in last 3 days
    url = MYURL + '/api/v1/accounts/1/sis_imports'
    d = datetime.now() - timedelta(days=3)
    header = {'Authorization': MYTOKEN}
    payload = {'per_page': 100, 'created_since': d}

    # Makes request
    r = requests.get(url, headers=header, params=payload)
    theJSON = json.loads(r.text)

    # Load latest SIS import. If it has been more than 10 hours, send an email.
    last = theJSON['sis_imports'][0]['created_at']
    target = datetime.now() - timedelta(hours=10)
    dLast = datetime.strptime(last, "%Y-%m-%dT%H:%M:%SZ")
    dLast = dLast.replace(tzinfo=pytz.UTC)

    pacific = pytz.timezone('US/Pacific')
    loc_target = pacific.localize(target)
    utc_target = loc_target.astimezone(pytz.utc)

    if dLast < utc_target:
        sendAlert(f"Canvas has not started an import in over 10 hours")

    # get current directories; If it fails I have to unlock the drive.
    try:
        top = next(os.walk('Z:/sis-canvas/'))
    except StopIteration as e:
        sendAlert(f"Z: drive is locked.")
        raise

    # Read the sis information.
    for sis in theJSON['sis_imports']:
        if str(sis['id']) not in top[1]:
            # If import is not done, don't process
            if sis['progress'] > 0 and sis['progress'] < 100:
                continue

            # Create directory name of SIS import id
            os.mkdir(f"Z:/sis-canvas/{sis['id']}")
            fn = f"Z:/sis-canvas/{sis['id']}/"

            # Dump the logfile into directory
            with open(f"{fn}log.json", 'w') as outfile:
                json.dump(sis, outfile)

            # If number of files is less than 6 send warning email
            check = sis['data'].get('supplied_batches', None)
            if check is None or len(check) < 6:
                sendEmail(sis['id'])

            # Download the attachements in SIS import
            for dl in sis['csv_attachments']:
                with requests.get(dl['url'], stream=True) as f:
                    fn = f"Z:/sis-canvas/{sis['id']}/"
                    with open(f"{fn}{dl['filename']}", 'wb') as fdl:
                        shutil.copyfileobj(f.raw, fdl)


if __name__ == "__main__":
    main()
