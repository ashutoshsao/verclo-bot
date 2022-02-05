# Discord verclo bot
-verclo stands for verification over cloud

-instructions to run this bot  
-1. create/add discord bot token from https://discord.com/developers/applications to token.txt  
-2. add maiil adress and password to config.txt  
-3. add server unique ID, tokenbot unique ID to bot.py  
-4. run bot.py script.

-following is the algorithm of how i am trying to make this bot work.  
-1. the bot wil work 24/7 on aws lambda  
-2. bot will take mail id from user and check if its valid  
-3. if yes, it will send a code to the user's mail and as him to input the code  
-4. if the code matches, the bot will assign the role to the user as verified  
-5.  the bot will save user's unique id,mail,etc in a mysql database with time

-current stage  
-I have checked the status that the bot stays online as long as the script runs, it can manage message

-vision  
-looking forwords to take this proejct forther and improve it for everyone
