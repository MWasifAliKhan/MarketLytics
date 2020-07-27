//IMPORTS
import pickle
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pandas as pd

#____________________________________________________________________________#

#Generating our API user tokens

def gsheet_api_check(SCOPES):
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
    return creds
#____________________________________________________________________________#

#Making the API call

from googleapiclient.discovery import build

def pull_sheet_data(SCOPES, SPREADSHEET_ID, RANGE_NAME):
    creds = gsheet_api_check(SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        rows = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                  range=RANGE_NAME).execute()
        data = rows.get('values')
        print("COMPLETE: Data copied")
        return data
#____________________________________________________________________________#


#Getting the data

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '13xtlQ-djoaj_QfX_H8TwMuZk4CUnEqiim7BO2eqrAvI'
RANGE_NAME = 'A1:A42'
data = pull_sheet_data(SCOPES, SPREADSHEET_ID, RANGE_NAME)

#___A little cleaning required, probably even a better way to do this___#

sep_data = []
for i in range(len(data)):
    sep_data.append(str(data[i]).split('_'))
    sep_data[i][0] = str(sep_data[i][0]).replace("[u'","")
    sep_data[i][-1] = str(sep_data[i][-1]).replace("']", "")


#Optional
#pd.set_option('display.max_rows', None)
#pd.set_option('display.max_columns', None)
#___From list to Pandas DataFrame___#
df = pd.DataFrame(sep_data,columns=["Department","Campaign Code","Campagin Name","Start date","Channel","Optional element (1)","Optional element (2)","Optional element (3)","Optional element (4)","Optional element (5)","Optional element (6)","Optional element (7)"])

print(df.head())
