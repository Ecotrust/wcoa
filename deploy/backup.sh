#!/bin/bash
today=`date +%B_%d_%Y`

/usr/bin/pg_dump -Fc ocean_portal > /home/backup/ocean_portal-$today.sql
