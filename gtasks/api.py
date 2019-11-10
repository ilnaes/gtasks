from __future__ import print_function
import pickle
import os.path
from datetime import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.


class Connection:
    SCOPES = ['https://www.googleapis.com/auth/tasks']
    FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

    def __init__(self, q):
        self.global_events = q

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

    def add_task(self, tasklist, task):
        results = self.service.tasks().insert(tasklist=tasklist, body=task).execute()
        return results['id']
    
    def complete_task(self, tasklist, taskid):
        task = self.service.tasks().get(tasklist=tasklist, task=taskid).execute()
        task['status'] = 'completed'

        result = self.service.tasks().update(tasklist=tasklist, task=taskid, body=task).execute()
        return result['completed']

    def get_lists(self):
        results = self.service.tasklists().list(maxResults=10).execute()
        items = results.get('items', [])
        self.global_events.put(('LISTS',
                                [[x['title'], x['id'], None] for x in items]))

    def get_tasks(self, id):
        res = self.service.tasks().list(tasklist=id, showCompleted=False).execute()
        res = res.get('items', [])
        tasks = [[t['title'], t['id'], datetime.strptime(t['due'], Connection.FORMAT)]
                 for t in res]
        tasks.sort(key=(lambda x: x[2]))
        self.global_events.put(('TASKS', (id, tasks)))
