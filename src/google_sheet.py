import pandas as pd
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import gspread
import os
import pickle

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

creds = None
# Token file stores user's access and refresh tokens
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)

# If no valid credentials, let user log in
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            r'C:\Users\spamj\Documents\Code\Python\Fin_Email_To_DB\client_secret_668101383803-6251gqcs6u3eku7gcsbqq4sd4opjmbt3.apps.googleusercontent.com.json',
            SCOPES)
        creds = flow.run_local_server(port=0)
    
    # Save credentials for next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

# Use credentials with gspread
client = gspread.authorize(creds)
sheet = client.open("test").sheet1
df = pd.DataFrame(sheet.get_all_records())
