from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1M31oyvu16W-2ndPq3pRrzKlIovIwu7DrmkOp9jvZA74'
SAMPLE_RANGE_NAME = 'Sheet1!A2:E17'

class Node:
    def __init__(self):
        self.l = None
        self.r = None
        self.u = None
        self.d = None

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
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

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    map = [None] * len(values)
    grid = ""
    
#    print(len(map))
    
    if not values:
        print('No data found.')
    else:
        for row in values:
            for i in range(len(row)):
                if row[i] is u'':
                    row[i] = None
                else:
                    row[i] = int(row[i])
                if len(row) is 4:
                    row.append(None)
#            print('%s: %s, %s, %s, %s' % (row[0], row[1], row[2], row[3], row[4]))
            n = row[0]
            map[n] = Node()
            map[n].l = row[1]
            map[n].r = row[2]
            map[n].u = row[3]
            map[n].d = row[4]

#    for node in map:
#        print('%s %s %s %s' % (node.l, node.r, node.u, node.d))
            
    # find the top left corner
    n = len(map)/2
    while map[n].u is not None or map[n].l is not None:
        if map[n].u is not None:
            n = map[n].u
        if map[n].l is not None:
            n = map[n].l

    while True:
        while map[n].r is not None:
            grid = grid + str(n) + ' '
#            print('%s' % n)
            n = map[n].r

        grid = grid + str(n) + '\n'
#        print('%s' % n)
        
        if map[n].d is not None:
            n = map[n].d
            while map[n].l is not None:
                n = map[n].l
        else:
            break    

    print(grid)
if __name__ == '__main__':
    main()
