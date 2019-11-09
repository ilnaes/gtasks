from __future__ import print_function
import pickle
import os.path
import datetime as dt
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.


class Connection:
    SCOPES = ['https://www.googleapis.com/auth/tasks']
    FORMAT = "%Y-%m-%dT%H:%M"

    def __init__(self, eventbox):
        self.global_events = eventbox

        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('../token.pickle'):
            with open('../token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    '../credentials.json', Connection.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('../token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('tasks', 'v1', credentials=creds)

    def get_lists(self):
        results = self.service.tasklists().list(maxResults=10).execute()
        items = results.get('items', [])
        self.global_events.set(('ITEMS',
                                [(x['title'], x['id']) for x in items]))

    def list_tasks():
        # Call the Tasks API

        for item in items:
            print(u'{0}'.format(item['title']))
            res = service.tasks().list(tasklist=item['id']).execute()
            res = res.get('items', [])
            tasks = [(t['title'], dt.datetime.strptime(t['due'], Connection.FORMAT))
                     for t in res]

            tasks.sort(key=(lambda x: x[1]))

            now = dt.datetime.now()

            for t in tasks:
                if t[1] < now:
                    print(u'\033[31m{1} -- {0}\033[0m'.format(t[0], t[1]))
                else:
                    print(u'\033[32m{1} -- {0}\033[0m'.format(t[0], t[1]))

        return tasks
