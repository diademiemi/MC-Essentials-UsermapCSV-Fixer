#!/usr/bin/env python3

# usermap.csv Fix NPC entries script made by DiaDemiEmi
# PLEASE READ README.md BEFORE USING

import re
import os
from dotenv import load_dotenv

# REPLACE userdata_location with the path to Essentials userdata directory
# REPLACE npc_location with the path to the Essentials NPC dump directory
# REPLACE usermap_file with path to usermap.csv

load_dotenv()
userdata_location = os.getenv('USERDATA_LOCATION')
npc_location = os.getenv('NPC_OUTPUT_LOCATION')
usermap_file = os.getenv('USERMAP_FILE')
output_file = os.getenv('OUTPUT_USERMAP_FILE')

# Create NPC_OUTPUT_LOCATION if it does not exist
if not os.path.exists(npc_location):
    os.makedirs(npc_location)

# Move all files containing "npc: true" to a seperate directory
for filename in os.listdir(userdata_location):
    file_path = os.path.join(userdata_location, filename)
    with open(file_path, "r") as f:
        if re.search('npc: true', f.readline()):
            os.rename(file_path, os.path.join(npc_location, filename))


# Load the contents of usermap_file into a variable called usermap
with open(usermap_file) as f:
    usermap = f.read()
print("There are {0} entries in usermap".format (usermap.count('\n')))

# Prepare variable which will be used to write the new usermap to temporarily
newusermap = ""
count = 0
# Read usermap line by line and per line find the username and UUID
# Check if this UUID appears in the NPC backup directory. If it does
# This username will be searched for by regex within the Essentials
# Userdata directory and upon match that filename will be used 
# to get the correct UUID, this UUID will then be saved as a substitute to the old one.
for line in usermap.splitlines(): 
    count += 1
    print("NUMBER OF LINES PROCESSED: {0}".format(count))
    username = re.findall('^[^,]+', line)[0]
    uuid = re.findall('(?<=,).*', line)[0]
    if os.path.isfile("{0}/{1}.yml".format(npc_location, uuid)):
        for filename in os.listdir(userdata_location):
            file_path = os.path.join(userdata_location, filename)
            with open(file_path, "r") as f:
                if re.search('lastAccountName: '+username+'\n', f.read(), flags=re.IGNORECASE):
                    newuuid = re.findall('^[^.yml]+', filename)[0]
                    newusermap += username + "," + newuuid + "\n"
                    print("The new UUID for {0} is {1}, changed from {2}".format(username, newuuid, uuid))
                    break
    # If this player does not have an NPC file, write the line as is
    else:
        print("Player {0} has no NPC file.".format(username))
        newusermap += line + "\n"

print("Begin Writing to file")
# Write the contents of the new usermap data into the usermap.csv file
print("There are {0} entries in new usermap".format (newusermap.count('\n')))
with open(output_file, 'w') as f:
    f.write(newusermap)