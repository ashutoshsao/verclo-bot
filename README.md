# Discord verclo bot
-verclo stands for verification over cloud

-Instructions to run this bot  
-1. create/add discord bot token from https://discord.com/developers/applications to token.txt  
-2. add sender's mail adress and password to config.py 
-3. add server unique ID, tokenbot unique ID to bot.py  
-4. run bot.py script.

-Following is the algorithm of how I am trying to make this bot work.  
-1. the bot will work 24/7 on aws lambda  
-2. bot will take mail id from user and check if its valid  
-3. if yes, it will send a code to the user's mail and ask him to input the code  
-4. if the code matches, the bot will assign the role to the user as verified  
-5. the bot will save user's unique id,mail,etc in a mysql database with time

-current stage  
-I have checked the status that the bot stays online as long as the script runs, it can manage messages

-vision  
-looking forwords to take this proejct forther and improve it for everyone
