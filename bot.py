"""for verclo-bot bot"""

"""for discord input/output"""

from random import randint
from turtle import delay
import discord
import asyncio
import random

def read_token():
    with open('token.txt','r') as f:
        lines = f.readlines()
        return lines[0].strip()
codex=random.randint(100000,999999)
print("OTP=",codex)
token = read_token()
client = discord.Client()
@client.event
async def on_message(message):
    id = client.get_guild('server unique ID')
    valid_owner_id = ['tokenbot unique ID']
    
    if str(message.author.id) in valid_owner_id:
        ticketno = str(message.channel)
        channelid = (message.channel.id)
        status = "ticket created"
        await message.delete(delay=None)
        print(status)    
    if(status=="ticket created" and message.channel.id==channelid):
        embed1 = discord.Embed(
            title = 'Welcome to our verification process',
            description = '',
            colour = 'color in hex'
        )
        embed1.set_thumbnail(url='url here')
        embed1.add_field(name='TO Proceed further in the verification process, enter your emailid [@gmail.com]',value='we are storing the emails in the database for security purposes')

        await message.channel.send(embed = embed1)
        status= "sendmailmessage"
        #print(ticketno)
        #print(channelid)
        print(status)   
    userid = message.author.id
    if(message.author.id == userid and status == 'mailmessage'):
        import re
        email = message.content
        regex = r'\b([a-zA-Z0-9]+)([\.{1}])?([a-zA-Z0-9]+)\@gmail([\.])com\b'
        print(email)
        if(re.fullmatch(regex, email)):
            #Valid Email
            await message.channel.send(f"""we will message you here, after sending an email to {email} with OTP, so wait for our message.""")
            status = 'emailvalid'
            print (status)
            
            """for email input/output"""

            import smtplib
            from email.mime.multipart import MIMEMultipart
            from email.mime.text import MIMEText
            
            from config import ADDRESS,PASSWORD

            def send_msg(sender, to, subject, body):
                msg = MIMEMultipart()
                msg['From']=sender
                msg['To']=to
                msg['subject']=subject
                msg.attach(MIMEText(body, "plain"))
                s.send_message(msg)            

            if __name__=='__main__':
                s = smtplib.SMTP(host='smtp.gmail.com', port=587)
                s.starttls()
                s.login(ADDRESS, PASSWORD)

                send_msg(ADDRESS,
                email,
                "verification code for "verclo-bot" server",
                "hi,\nplease enter the code {codex} on the email verification channel to access the server.\nif you didn't request this code, you can safely ignore this email. someone else might have typed your email address by mistake.\n\nDon't reply to this mail id if you have any problem,\nmail: 'your email adress'\n\nThanks!\n'your name'")

                s.quit()
            await message.channel.send(f"""Okay, OTP has been sent at {email} , do check the spam and promitions.Please sen the OPT(withoutspace), you got 3 changes""")
            status = 'mailsent'
            
        
        else:
            #Invalid Email
            await message.channel.send(f"""the emailid {email} is invalid.""")
        if(status=="mailsent" and message.author.id == userid):
            otp=message.content
            while(1<4):
                if(otp == codex):
                    await message.channel.send(f"""Thank you for the verification, You are now verified.""")
                        


            
client.run(token)


