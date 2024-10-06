import os
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from sys import argv
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

        if os.path.isdir(item_path):#Check if folder
            folder_id = create_or_get_folder(service, item, parent_id)
            upload_files_in_folder(service, item_path, folder_id)
        else:# If file
            file_metadata = {'name': item, 'parents': [parent_id]}
            Upload = MediaFileUpload(item_path)
            # Check if file already exists
            file_check = service.files().list(
                q=f"name='{item}' and '{parent_id}' in parents", spaces="drive"
            ).execute()
            if file_check['files']:
                # File exists, check its size
                file_id = file_check["files"][0].get("id")
                file_data = service.files().get(fileId=file_id, fields="id, name, mimeType, size").execute()
                cloud_size = int(file_data.get("size"))
                local_size = os.path.getsize(item_path)

                if cloud_size != local_size:
                    # Replace existing file
                    service.files().delete(fileId=file_id).execute()
                    service.files().create(body=file_metadata, media_body=Upload, fields='id').execute()
                    print(f"File {item} replaced with new version.")
            else:
                # Upload new file if it doesn't exist
                service.files().create(body=file_metadata, media_body=Upload, fields='id').execute()
                print(f"New File {item} uploaded.")


def Folder(service, folder):
    # Check if main folder exists on Drive
    folder_id = create_or_get_folder(service, "Backup_2024")
    upload_files_in_folder(service, folder, folder_id)

# Storage Info
def Storage_Info(service):
    about = service.about().get(fields="storageQuota").execute()
    S_limit=int(about["storageQuota"]["limit"])/(1024**3)
    S_used=int(about["storageQuota"]["usage"])/(1024**3)
    Drive_use=int(about["storageQuota"]["usageInDrive"])/(1024**3)
    Drive_trash=int(about["storageQuota"]["usageInDriveTrash"])/(1024**3)
    print("-"*100)
    print("-------------Storage Information-------------")
    print(f"Storage Limit: {S_limit:.2f}GB")   
    print(f"Storage Usage: {S_used:2f}GB")   
    print(f"Storage Usage in Drive: {Drive_use:2f}")   
    print(f"Storage Usage in Trash: {Drive_trash:2f}")

def starter_code():
    service = Basic_configuration()
    if len(argv)!=1:
        if os.path.isdir(argv[1]):#Get Folders from command line
            for folder in range(1,len(argv)):
                print(f"Checking Path: {argv[folder]}\n")
                Folder(service,argv[folder])
        else:#File containing folder paths
            with open(argv[1],'r') as paths:
                for folder in paths.readlines():
                    print(f"Checking Path: {folder}\n")
                    folder=folder.strip("\n")
                    Folder(service,folder)
    else:
        folder=input("Enter Path of folder:")
        Folder(service,folder)
    Storage_Info(service)

    
if __name__ == "__main__":
    starter_code()
