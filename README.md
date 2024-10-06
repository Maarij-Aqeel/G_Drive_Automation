# Google Drive Backup Automation

A Python tool for automating Google Drive backups, replacing existing files if updated, listing Drive contents, and displaying storage information.

## Features
- Automatic Backup: Recursively upload folders to Google Drive, creating directories as needed.
- File Replacement: Detects and replaces files if local versions differ from Drive versions.
- Storage Monitoring: Displays Drive storage usage and quota.-
- Drive Content Listing: Lists all files and folders in your Drive, including subfolders.
- Command Line Interface: Flexible and easy-to-use CLI options for different tasks.

## Prerequisites

  * __Python__ : Make sure you have Python 3 installed on your system.
  * __Google Drive API Credentials__:

    * Go to the [Google Developers Console](https://cloud.google.com).
    * Create a project and enable the Google Drive API.
    * Create OAuth 2.0 credentials and download the credentials.json file.

  * __Python Libraries__: Install required libraries:


    ```bash
    pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
     

## Setup

  * __Clone the Repository__:


    ```bash
     git clone https://github.com/yourusername/google-drive-backup.git
    cd google-drive-backup 

  * __Add Your Credentials__: Place your ` credentials.json ` file in the root directory of the project.

  * __Authenticate__: On the first run, a browser window will open for you to authenticate with Google. This creates a `Token.json` file for future logins.

## Usage

  Run the script from the command line with various options:


 ```python 
 python main.py [options] [folder_path(s) or file_path]
 ```

## Options

    --help or -h: Show the help menu.
    -storage: Display Google Drive storage information.
    -list: List all files and folders in your Google Drive.
    [folder_path]: Backup specific folders from your system.
    [file_path]: Backup folders listed in a text file (one path per line).

## Examples

  __Backup a Folder:__


  ```python
  python main.py /path/to/your/folders
```

  __Backup Multiple Folders:__


   ```python
  python main.py /path/to/folder1 /path/to/folder2
 ```

  __Show Storage Information:__


   ```python
  python main.py -storage
 ```

__List Drive Contents:__



   ```python
  python main.py -list
 ```

## Notes

* Ensure that `credentials.json` and `Token.json` are kept private to prevent unauthorized access.
* The `Token.json` file is created after the first run and used for subsequent logins without re-authentication.
