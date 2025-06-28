async def start_verification(self, message, user_id, channel_id):
        """Start the verification process (self-initiated)"""
        try:
            # Check if user is already in verification process
            if user_id in self.user_states:
                await message.channel.send("❌ You are already in the verification process. Please complete it first.")
                return
            
            # Delete the command message if possible
            try:
                await message.delete()
            except:
                pass  # Ignore if can't delete (might be in DMs)
            
            print(f"Verification started for user {user_id}")
            
            # Set user state
            self.user_states[user_id] = "awaiting_email"
            self.user_channels[user_id] = channel_id
            
            # Send welcome embed
            embed = discord.Embed(
                title='Welcome to our verification process',
                description=f'{message.author.mention}, please follow the steps below to get verified.',
                color=0x00ff00
            )
            embed.add_field(
                name='Step 1: Email Verification',
                value='Please enter your email address (must be @gmail.com)\nWe store emails in our database for security purposes.',
                inline=False
            )
            embed.set_footer(text="Verification Bot")
            
            await message.channel.send(embed=embed)
            
        except Exception as e:
            print(f"Error starting verification: {e}")
            await message.channel.send("❌ Error starting verification. Please try again.")"""Discord Verification Bot - Fixed Version"""
import discord
import asyncio
import random
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import ADDRESS, PASSWORD

class VerificationBot:
    def __init__(self):
        # Store user verification states
        self.user_states = {}
        self.user_channels = {}
        self.user_emails = {}
        self.user_otps = {}
        self.user_attempts = {}
        
        # Bot configuration
        self.valid_owner_ids = ['your_bot_owner_id_here']  # Replace with actual ID
        self.server_id = 'your_server_id_here'  # Replace with actual server ID
        self.verification_channel_names = ['verification', 'verify', 'welcome']  # Allowed channel names
        
        # Set up Discord client with intents
        intents = discord.Intents.default()
        intents.message_content = True
        self.client = discord.Client(intents=intents)
        
        # Register events
        self.client.event(self.on_ready)
        self.client.event(self.on_message)
    
    def read_token(self):
        """Read bot token from file"""
        try:
            with open('token.txt', 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            print("Error: token.txt file not found!")
            return None
    
    async def on_ready(self):
        """Called when bot is ready"""
        print(f'{self.client.user} has connected to Discord!')
    
    async def on_message(self, message):
        """Handle incoming messages"""
        # Ignore bot's own messages
        if message.author == self.client.user:
            return
        
        user_id = str(message.author.id)
        channel_id = message.channel.id
        content = message.content.strip().lower()
        
        # Check for verification command
        if content == "!verify" or content == "verify":
            # Only allow in specific verification channels or DMs
            if self.is_verification_channel(message.channel):
                await self.start_verification(message, user_id, channel_id)
            else:
                await message.channel.send("❌ Please use the verification channel or DM me to verify.")
            return
        
        # Owner commands
        if user_id in self.valid_owner_ids:
            if content.startswith("!start_verify "):
                # Owner can start verification for specific user: !start_verify @user
                await self.handle_owner_command(message)
                return
        
        # Handle user responses based on their current state
        if user_id in self.user_states:
            await self.handle_user_response(message, user_id)
    
    def is_verification_channel(self, channel):
        """Check if channel is allowed for verification"""
        # Allow DMs
        if isinstance(channel, discord.DMChannel):
            return True
        
        # Allow specific channel names
        if channel.name.lower() in self.verification_channel_names:
            return True
        
        return False
    
    async def handle_owner_command(self, message):
        """Handle owner commands like !start_verify @user"""
        if message.mentions:
            target_user = message.mentions[0]
            user_id = str(target_user.id)
            
            # Check if user is already in verification process
            if user_id in self.user_states:
                await message.channel.send(f"❌ {target_user.mention} is already in verification process.")
                return
            
            # Start verification for target user
            await message.channel.send(f"✅ Starting verification process for {target_user.mention}")
            await self.start_verification_for_user(message, user_id, target_user)
        else:
            await message.channel.send("❌ Please mention a user: `!start_verify @username`")
    
    async def start_verification_for_user(self, message, user_id, target_user):
        """Start verification for a specific user (called by owner)"""
        channel_id = message.channel.id
        
        # Set user state
        self.user_states[user_id] = "awaiting_email"
        self.user_channels[user_id] = channel_id
        
        # Send welcome embed
        embed = discord.Embed(
            title=f'Verification Process for {target_user.display_name}',
            description=f'{target_user.mention}, please follow the steps below to get verified.',
            color=0x00ff00
        )
        embed.add_field(
            name='Step 1: Email Verification',
            value='Please enter your email address (must be @gmail.com)\nWe store emails in our database for security purposes.',
            inline=False
        )
        embed.set_footer(text="Verification Bot")
        
        await message.channel.send(embed=embed)
    
    async def handle_user_response(self, message, user_id):
        """Handle user responses based on their current state"""
        current_state = self.user_states.get(user_id)
        
        if current_state == "awaiting_email":
            await self.handle_email_input(message, user_id)
        elif current_state == "awaiting_otp":
            await self.handle_otp_input(message, user_id)
    
    async def handle_email_input(self, message, user_id):
        """Handle email input from user"""
        email = message.content.strip()
        
        # Validate email format
        email_regex = r'\b[a-zA-Z0-9._%+-]+@gmail\.com\b'
        
        if re.fullmatch(email_regex, email):
            # Valid email
            self.user_emails[user_id] = email
            self.user_states[user_id] = "awaiting_otp"
            self.user_attempts[user_id] = 3  # Give user 3 attempts
            
            # Generate OTP
            otp = random.randint(100000, 999999)
            self.user_otps[user_id] = str(otp)
            
            print(f"Generated OTP for {email}: {otp}")
            
            try:
                # Send email
                await self.send_verification_email(email, otp)
                await message.channel.send(
                    f"✅ OTP has been sent to {email}\n"
                    f"Please check your inbox (and spam folder) and enter the 6-digit code.\n"
                    f"You have 3 attempts remaining."
                )
            except Exception as e:
                print(f"Error sending email: {e}")
                await message.channel.send(
                    "❌ Error sending email. Please try again later or contact an administrator."
                )
                # Reset state on email error
                self.user_states[user_id] = "awaiting_email"
        else:
            # Invalid email
            await message.channel.send(
                f"❌ The email '{email}' is invalid. Please enter a valid @gmail.com address."
            )
    
    async def handle_otp_input(self, message, user_id):
        """Handle OTP input from user"""
        entered_otp = message.content.strip()
        correct_otp = self.user_otps.get(user_id)
        attempts_left = self.user_attempts.get(user_id, 0)
        
        if entered_otp == correct_otp:
            # Correct OTP
            await message.channel.send(
                "🎉 Thank you for verification! You are now verified and have access to the server."
            )
            
            # Clean up user data
            self.cleanup_user_data(user_id)
            
            # Here you could add role assignment or other verification completion tasks
            await self.assign_verified_role(message.author)
            
        else:
            # Incorrect OTP
            attempts_left -= 1
            self.user_attempts[user_id] = attempts_left
            
            if attempts_left > 0:
                await message.channel.send(
                    f"❌ Incorrect OTP. You have {attempts_left} attempt(s) remaining."
                )
            else:
                await message.channel.send(
                    "❌ Maximum attempts exceeded. Please start the verification process again."
                )
                self.cleanup_user_data(user_id)
    
    async def send_verification_email(self, email, otp):
        """Send verification email with OTP"""
        def send_email():
            try:
                # Create message
                msg = MIMEMultipart()
                msg['From'] = ADDRESS
                msg['To'] = email
                msg['Subject'] = 'Verification code for Discord Server'
                
                body = f"""
Hi there!

Please enter the code {otp} in the Discord verification channel to access the server.

If you didn't request this code, you can safely ignore this email. Someone else might have typed your email address by mistake.

Don't reply to this email. If you have any problems, please contact an administrator.

Thanks!
Your Discord Server Team
                """
                
                msg.attach(MIMEText(body, 'plain'))
                
                # Send email
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(ADDRESS, PASSWORD)
                server.send_message(msg)
                server.quit()
                
                return True
            except Exception as e:
                print(f"Email sending error: {e}")
                return False
        
        # Run email sending in thread to avoid blocking
        loop = asyncio.get_event_loop()
        success = await loop.run_in_executor(None, send_email)
        
        if not success:
            raise Exception("Failed to send email")
    
    async def assign_verified_role(self, user):
        """Assign verified role to user after successful verification"""
        try:
            guild = user.guild
            verified_role = discord.utils.get(guild.roles, name="Verified")  # Change role name as needed
            
            if verified_role:
                await user.add_roles(verified_role)
                print(f"Assigned verified role to {user.display_name}")
            else:
                print("Verified role not found - please create a role named 'Verified'")
                
        except Exception as e:
            print(f"Error assigning role: {e}")
    
    def cleanup_user_data(self, user_id):
        """Clean up user verification data"""
        keys_to_remove = [user_id]
        for key in keys_to_remove:
            self.user_states.pop(key, None)
            self.user_channels.pop(key, None)
            self.user_emails.pop(key, None)
            self.user_otps.pop(key, None)
            self.user_attempts.pop(key, None)
    
    def run(self):
        """Start the bot"""
        token = self.read_token()
        if token:
            try:
                self.client.run(token)
            except Exception as e:
                print(f"Error running bot: {e}")
        else:
            print("Could not read token. Bot cannot start.")

# Create and run the bot
if __name__ == '__main__':
    bot = VerificationBot()
    bot.run()
