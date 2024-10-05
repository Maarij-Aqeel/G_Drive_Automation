import os
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

#Basic configuration
Scopes=["https://www.googleapis.com/auth/drive"]
creds=None
if os.path.exists("Token.json"):
    creds=Credentials.from_authorized_user_file("Token.json",scopes=Scopes)
if not creds or not creds.valid:
    if creds  and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow=InstalledAppFlow.from_client_secrets_file("credentials.json",scopes=Scopes)
        creds=flow.run_local_server(port=8080)
    with open ("Token.json","w") as token:
        token.write(creds.to_json())

service= build('drive','v3',credentials=creds)

# Check if folder exists on Google Drive
response=service.files().list(
    q="name='Backup_2024' and mimeType='application/vnd.google-apps.folder'",
    spaces="drive"
).execute()
#If doesn't exist Create it
if not response["files"]:
    file_metadata={"name":"Backup_2024","mimeType":"application/vnd.google-apps.folder"}
    file= service.files().create(body=file_metadata,fields="id").execute()
    folder_id=file.get("id")
else:
    folder_id=response["files"][0]["id"]

for file in os.listdir('Test_backups'):
    file_metadata={
        'name':file,
        'parents':[folder_id]
    }

    Upload=MediaFileUpload(f'Test_backups/{file}')
    upload_files=service.files().create(body=file_metadata,media_body=Upload,fields='id').execute()
    print(f"Backed_up file {file} Successfully")