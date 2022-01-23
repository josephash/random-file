# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START sheets_quickstart]
from __future__ import print_function

import os.path
from datetime import datetime
from threading import Thread

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly',
'https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1bTu9VOY2n-gD3ztjfsf2LX2JSrBFXyJ_F1sJxS-JC6E'
RANGE_NAME = "RawData!A1:B1"


def main(tag, scantime):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=RANGE_NAME).execute()
        values = result.get('values', [])

        # Add values
        newvalues = {
            "majorDimension": "DIMENSION_UNSPECIFIED",
            "range": RANGE_NAME,
            "values": 
            [
                [scantime, tag]
            ]
        }
        service.spreadsheets().values().append(spreadsheetId=SPREADSHEET_ID,
                                    range=RANGE_NAME,
                                    valueInputOption='USER_ENTERED',
                                    includeValuesInResponse=False,
                                    body=newvalues
                                    ).execute()
        #print("Done!")
    except HttpError as err:
        print(err)

while True:
    newtag = str(input("Tag:"))
    if newtag == "exit":
        exit()
    newtime = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    if __name__ == '__main__':
        thread = Thread(target = main, args = (newtag, newtime))
        thread.start()