from __future__ import print_function
import pickle
import os.path
import datetime as dt
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/tasks']
FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


def list_tasks():
    """Shows basic usage of the Tasks API.
    Prints the title and ID of the first 10 task lists.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('tasks', 'v1', credentials=creds)

    # Call the Tasks API
    results = service.tasklists().list(maxResults=10).execute()
    items = results.get('items', [])

    if not items:
        print('No task lists found.')
    else:
        print('Task lists:')
        for item in items:
            print(u'{0}'.format(item['title']))
            res = service.tasks().list(tasklist=item['id']).execute()
            res = res.get('items', [])
            tasks = [(t['title'], dt.datetime.strptime(t['due'], FORMAT))
                     for t in res]

            tasks.sort(key=(lambda x: x[1]))

            now = dt.datetime.now()

            for t in tasks:
                if t[1] < now:
                    print(u'\033[31m{1} -- {0}\033[0m'.format(t[0], t[1]))
                else:
                    print(u'\033[32m{1} -- {0}\033[0m'.format(t[0], t[1]))

    return tasks


if __name__ == '__main__':
    list_tasks()
