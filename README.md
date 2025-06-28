# Verclo Bot - Discord Verification Bot

A Discord verification bot that uses email-based OTP verification to grant server access. Verclo stands for "Verification Over Cloud" - designed to run 24/7 on cloud platforms like AWS Lambda.

## Tech Stack

- Backend: Python, Discord.py, asyncio, smtplib
- Database: MySQL (planned)
- Cloud: AWS Lambda (planned deployment)
- Email Service: Gmail SMTP

---

## Project Structure

```bash
.
├── bot.py              # Main bot logic and verification system
├── config.py           # Email configuration (sender credentials)
├── token.txt           # Discord bot token
└── README.md           # Project documentation
```

---

## Features

### 1. Email-Based Verification
- Users provide Gmail addresses for verification
- 6-digit OTP sent to user's email
- 3 attempts allowed per verification session
- Automatic role assignment upon successful verification

### 2. Multi-Channel Support
- Works in designated verification channels (`verification`, `verify`, `welcome`)
- Supports DM verification for privacy
- Owner commands for manual verification initiation

### 3. Security Features
- Email validation (Gmail only)
- OTP expiration and attempt limits
- User state management to prevent duplicate processes
- Database storage for audit trails (planned)

---

## Getting Started

### Prerequisites

- Python 3.7+
- Discord bot token
- Gmail account with app password enabled

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/verclo-bot.git
   cd verclo-bot
   ```

2. **Install dependencies**
   ```bash
   pip install discord.py asyncio
   ```

3. **Configure the bot**
   
   **Step 1:** Add your Discord bot token to `token.txt`
   ```
   your_discord_bot_token_here
   ```
   
   **Step 2:** Update `config.py` with your email credentials
   ```python
   ADDRESS = "your_email@gmail.com"
   PASSWORD = "your_app_password"
   ```
   
   **Step 3:** Update `bot.py` with your server details
   ```python
   self.valid_owner_ids = ['your_discord_user_id']
   self.server_id = 'your_server_id'
   ```

4. **Run the bot**
   ```bash
   python bot.py
   ```

---

## Usage

### For Users
- Type `!verify` or `verify` in verification channels
- Enter your Gmail address when prompted
- Check email for 6-digit OTP code
- Enter the code to complete verification

### For Server Owners
- `!start_verify @username` - Manually start verification for a user
- Bot automatically assigns "Verified" role upon successful verification

---

## Core Concepts

### Verification Flow
1. **Initiation**: User runs `!verify` command
2. **Email Input**: User provides Gmail address
3. **OTP Generation**: 6-digit code generated and emailed
4. **Verification**: User enters OTP (3 attempts max)
5. **Role Assignment**: "Verified" role granted on success

### State Management
- `awaiting_email`: User needs to provide email
- `awaiting_otp`: User needs to enter OTP code
- Automatic cleanup on completion or failure

### Email System
- Gmail SMTP integration
- Professional verification email template
- Error handling for delivery failures

---

## Configuration Options

### Channel Settings
```python
self.verification_channel_names = ['verification', 'verify', 'welcome']
```

### Role Assignment
```python
verified_role = discord.utils.get(guild.roles, name="Verified")
```

### OTP Settings
- 6-digit numeric codes
- 3 attempts per verification
- Immediate cleanup on max attempts

---

## Roadmap

### Current Stage ✅
- [x] Basic bot functionality and message handling
- [x] Email-based OTP verification system
- [x] Role assignment on successful verification
- [x] Multi-channel and DM support

### Planned Features 🚀
- [ ] AWS Lambda deployment for 24/7 operation
- [ ] MySQL database integration for user data storage
- [ ] Advanced security features and rate limiting
- [ ] Web dashboard for verification management
- [ ] Multiple email provider support
- [ ] Verification analytics and reporting

---

## Dependencies

- **discord.py**: Discord API wrapper
- **asyncio**: Asynchronous programming support
- **smtplib**: Email sending functionality
- **re**: Email validation regex patterns

---

## Security Notes

- Store sensitive credentials in environment variables for production
- Use app passwords for Gmail integration
- Regularly rotate bot tokens and email passwords
- Monitor verification logs for suspicious activity

---

## License

This project is open-source and available under the MIT License.

---

## Contributing

Pull requests and suggestions are welcome! For major changes, please open an issue first to discuss what you'd like to change.

### Development Guidelines
- Follow Python PEP 8 style guidelines
- Add error handling for all external API calls
- Test verification flow thoroughly before submitting
- Document any new configuration options

---

## Author

- Ashutosh Sao

Feel free to reach out for improvements or collaborations. Looking forward to taking this project further and improving it for everyone!
