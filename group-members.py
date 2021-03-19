#!/usr/bin/env python

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/admin.directory.group.readonly']

def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('admin', 'directory_v1', credentials=creds)

    groups = []

    params = {
        'fields': 'nextPageToken, groups(id, email)',
        'customer': 'my_customer',
    }
    while True:
        results = service.groups().list(**params).execute()

        groups += results.get('groups', [])

        params['pageToken'] = results.get('nextPageToken', None)
        if params['pageToken'] is None:
            break

    print(f"Found {len(groups)} groups")
    for group in groups:
        params = {
            'groupKey': group['id'],
            'fields': 'nextPageToken, members(email)',
        }
        while True:
            group_res = service.members().list(**params).execute()

            for member in group_res.get('members', []):
                print(f"{member['email']} in group {group['email']}")

            params['pageToken'] = group_res.get('nextPageToken', None)
            if params['pageToken'] is None:
                break

if __name__ == '__main__':
    main()
