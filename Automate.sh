#!/bin/bash

#Sleep 

#sleep 60

#Virtual Environment

#source /path/to/virtual/environment/

#Navigate to folder

cd /path/to/folder/

#Adding Timestamp
echo "Script started at $(date)" >> /path/to/log/file.txt
#Run Script
python3 main.py /path/to/folder/   >>  /path/to/log/file.txt 2>&1

#Ending 
echo "Script ended at $(date)" >> /path/to/log/file.txt

echo "--------------------------------------------------------------------------------------" >>  /path/to/log/file.txt

#Example of Automatically running on reboot in linux
@reboot /path/to/bash/file.sh >> /path/to/log/file.txt 2>&1
















#!/bin/bash

# Uncomment the following line if you are using a virtual environment
# source /path/to/your/venv/bin/activate

# Navigate to the directory where your Python script is located
cd /path/to/your/project

# Run the Python script with any necessary arguments
python3 main.py /path/to/your/folder -noreplace

# Optionally, redirect output to a log file if needed
# python3 main.py -storage >> /path/to/backup_log.txt 2>&1
