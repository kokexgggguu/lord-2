# Discord Bot - Python

A simple Discord bot built with Python using the discord.py library. This bot provides basic command handling, message responses, and interactive features for Discord servers.

## Features

- 🏓 **Ping Command** - Check bot responsiveness and latency
- ❓ **Help System** - Comprehensive help for all commands
- 📊 **Bot Information** - Display bot statistics and technical details
- 💬 **Echo Command** - Make the bot repeat messages
- 🧹 **Message Clearing** - Clear messages from channels (Admin only)
- 🏰 **Server Information** - Display detailed server statistics
- 🔔 **Mention Responses** - Bot responds when mentioned
- ⚠️ **Error Handling** - Comprehensive error handling with user-friendly messages
- 📝 **Logging** - Detailed logging for monitoring and debugging

## Prerequisites

- Python 3.8 or higher
- A Discord application and bot token
- Required Python packages (see installation steps)

## Installation

1. **Clone or download this project**
   ```bash
   git clone <repository-url>
   cd discord-bot
   ```

2. **Install required packages**
   ```bash
   pip install discord.py python-dotenv psutil
   ```

3. **Set up your Discord Bot**
   
   a. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
   
   b. Click "New Application" and give it a name
   
   c. Go to the "Bot" section in the left sidebar
   
   d. Click "Add Bot"
   
   e. Copy the bot token (keep this secret!)
   
   f. Under "Privileged Gateway Intents", enable:
      - Message Content Intent
      - Server Members Intent (optional)

4. **Configure the bot**
   
   a. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
   
   b. Edit `.env` and add your bot token:
   ```env
   DISCORD_BOT_TOKEN=your_actual_bot_token_here
   COMMAND_PREFIX=!
   ```

5. **Invite the bot to your server**
   
   a. In the Discord Developer Portal, go to "OAuth2" > "URL Generator"
   
   b. Select scopes: `bot` and `applications.commands`
   
   c. Select bot permissions:
      - Send Messages
      - Read Message History
      - Manage Messages (for clear command)
      - Use Slash Commands
      - Embed Links
      - Add Reactions
   
   d. Copy the generated URL and open it in your browser
   
   e. Select your server and authorize the bot

## Usage

### Running the Bot

```bash
python main.py
