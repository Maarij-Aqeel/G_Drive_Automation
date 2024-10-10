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
















