# review-maintenance
A splunk-sdk-python script to maintain the incident review KV store. 

Note you must install splunk-sdk-python first. Search github for splunk-sdk-python.

Review does maintenance on the incident_review collection for Splunk Enterprise Security. Using this script you can examine and optionally delete records from this collection. This script is suitable for CRON scheduling to enable periodic cleaning of the collection.

For example:
  python review.py --password mypsswd -D 90 -f --delete
  
  The above will delete all records more than 90 days old on the local server, using the admin account and port 8089. 

Syntax:
  review.py --host --port --username --password -HDM -q -f  --delete
  
  --host: Splunk server address, defaults to localhost 
  --port, splunkd port, defaults to 8089
  --username, defaults to admin
  --password, defaults to changeme
  
  -D: number of days
  -H: number of hours
  -M: number of minutes
  
The above time range flags are optional--if all are omitted, all records are selected (and optionally deleted). If more than one of D, H and/or M are used, they are added together to establish the datetime range. All records OLDER than this datetime will be selected.

 -q: quiet mode. Without this flag, the script will display the contents of the selected records to STDOUT.
 
 -f: force delete. Without this flag, the user is prompted to confirm deletion. Ignored if --delete is not used.
 
 --delete: deletes any records selected by the time range. If -f is used, records are immediately deleted with no prompt.
 
 
