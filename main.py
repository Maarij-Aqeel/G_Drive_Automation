import os
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Basic configuration
def Basic_configuration():
    Scopes = ["https://www.googleapis.com/auth/drive"]
    creds = None
    if os.path.exists("Token.json"):
        creds = Credentials.from_authorized_user_file("Token.json", scopes=Scopes)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", scopes=Scopes)
            creds = flow.run_local_server(port=8080)
        with open("Token.json", "w") as token:
            token.write(creds.to_json())
    service = build('drive', 'v3', credentials=creds)
    return service

#Create a folder if not already else get its id
def create_or_get_folder(service, folder_name, parent_id=None):
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'"
    if parent_id:
        query += f" and '{parent_id}' in parents"
    
    response = service.files().list(q=query, spaces="drive").execute()
    
    if not response["files"]:
        # If the folder does not exist, create it
        file_metadata = {"name": folder_name, "mimeType": "application/vnd.google-apps.folder"}
        if parent_id:
            file_metadata['parents'] = [parent_id]
        folder = service.files().create(body=file_metadata, fields="id").execute()
        print(f"Folder {folder_name} Uploaded!")
        return folder.get("id")
    else:
        # If it exists, return its ID
        return response["files"][0]["id"]

#Recursively upload files/Folders
def upload_files_in_folder(service, folder_path, parent_id):
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        
        if os.path.isdir(item_path):
            folder_id = create_or_get_folder(service, item, parent_id)
            upload_files_in_folder(service, item_path, folder_id)
        else:
            # If it's a file, upload it
            file_check = service.files().list(q=f"name='{item}' and '{parent_id}' in parents", spaces="drive").execute()
            if not file_check["files"]:
                file_metadata = {
                    'name': item,
                    'parents': [parent_id]
                }
                Upload = MediaFileUpload(item_path)
                service.files().create(body=file_metadata, media_body=Upload, fields='id').execute()
                print(f"File {item} uploaded to Folder {folder_path.split("/")[-1]}")

def Folder(service, folder):
    # Check if main folder exists on Drive
    folder_id = create_or_get_folder(service, "Backup_2024")
    upload_files_in_folder(service, folder, folder_id)

def starter_code():
    folder = input("Enter the path of the folder you want to backup: ")
    service = Basic_configuration()
    Folder(service, folder)

if __name__ == "__main__":
    starter_code()
