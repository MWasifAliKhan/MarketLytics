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






#____SAMPLE OUTPUT____#

#   Department Campaign Code Campagin Name  \
# 0       BIOX           WEB          BioX   
# 1         CM           GEN          BIOX   
# 2         CM           GEN          BIOX   
# 3       BIOX           WEB          BioX   
# 4         CM           GEN          BIOX   

#                              Start date                  Channel  \
# 0                              20192904           Qiagen Website   
# 1                                  0719                     SMOR   
# 2  IPA-OS-UGM-Cambridge2019-SaveTheDate                     0719   
# 3                              20191605  tv.qiagenbioinformatics   
# 4                                  0719                     SMOR   

#                Optional element (1) Optional element (2) Optional element (3)  \
# 0  Ingenuity Pathway Analysis (IPA)               BioxBA                 Must   
# 1                               IPA             LinkedIn                 None   
# 2                                EM                  CRM                 2924   
# 3                           Webinar               BioxBA                 Must   
# 4                               IPA              Twitter                 None   

#   Optional element (4) Optional element (5) Optional element (6)  \
# 0                  Win                    1                 BIOX   
# 1                 None                 None                 None   
# 2                 5104                 None                 None   
# 3                  Win                    1                 BIOX   
# 4                 None                 None                 None   

# Optional element (7)  
# 0                 None  
# 1                 None  
# 2                 None  
# 3                 None  
# 4                 None  

# Process finished with exit code 0

