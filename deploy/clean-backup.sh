#!/bin/bash

# get todays date
today=`date +%H_%B_%d_%Y`

echo "deleting the following files:" > /home/backup/logs/backup-cleanup_$today.txt
find /home/backup -mtime +3 -type f >> /home/backup/logs/backup-cleanup_$today.txt
find /home/backup -mtime +3 -type f -delete
