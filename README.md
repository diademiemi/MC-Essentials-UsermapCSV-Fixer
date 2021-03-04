# Script to remove NPC files in the Essentials userdata directory and correct usermap.csv accordingly

This script was made after a plugin broke our Essentials userdata directory. It made many NPC files which caused /seen, balance and other features to malfunction.  
Upon removing these YML files with a simple bash script, we noticed Essentials regenerated these, upon further investigation, we noticed the fake UUIDs generated for these NPC files were still stored in usermap.csv.  

### EXAMPLE

In the examples/ directory in this repository, you can see a fake usermap.csv file, userdata directory and the output which this script generated.  
You can use this to check if you are experiencing the same issue, and if this script will help you.  

### How to use

Modify the .env file in this directory and add change the values to the proper locations for your setup. Then run the script! This can take a while, so I recommend running it in a program like tmux.  

### DISCLAIMERS

This script can take a long time to run. On our usermap.csv of about 25K lines, it took about 45 minutes. This is because it needs to *search* through the userdata directory, which can take a long time depending on how many files you have in there.  
We ran this script on a copy of the userdata directory and usermap file, and copied it's output to the server later during a scheduled restart. Any missing data (Such as from players who joined since copying the files) will be automatically added again by Essentials, and it seems to have caused no issues.  

This script only writes the output once it is completely done, it will print how many lines usermap.csv is at the beginning and print its progress so you can see the speed.  

### HOW IT WORKS

This script searches through the userdata directory and moves all the NPC files to a backup directory (We have noticed some players who were affected had their marbles deposited / withdrawn from this fake file instead, for that reason it is probably wise to keep these files and inspect them).  
When this is done, it goes through each line in usermap.csv, then it checks if this UUID appears in the NPC directory made previously. If they do, this means this UUID is incorrect and points to a fake NPC file. It then grabs the username and searches through the now correct userdata directory fot the username, upon a match, it grabs the UUID from their actual file, and saves it as their new UUID.  

