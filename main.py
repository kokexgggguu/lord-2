#!/usr/bin/env python3
"""
Discord Bot Main Entry Point with Web Interface
A comprehensive Discord server management platform with Flask web dashboard
"""

import os
import threading
import logging
import asyncio
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def run_bot():
    """Run the Discord bot"""
    try:
        import bot
        asyncio.run(bot.run_bot())
    except Exception as e:
        logger.error(f"Error running Discord bot: {e}")

def run_flask_app():
    """Run the Flask web application"""
    try:
        from app import app
        app.run(host="0.0.0.0", port=5000, debug=False)
    except Exception as e:
        logger.error(f"Error running Flask app: {e}")

if __name__ == "__main__":
    logger.info("Starting Discord Bot Manager...")
    
    # Check for required environment variables
    if not os.getenv('DISCORD_TOKEN'):
        logger.warning("DISCORD_TOKEN not found. The bot will not function without it.")
        logger.info("Please set DISCORD_TOKEN in your .env file or environment variables.")
    
    try:
        # Start Discord bot in a separate thread
        bot_thread = threading.Thread(target=run_bot, daemon=True, name="DiscordBot")
        bot_thread.start()
        logger.info("Discord bot thread started")
        
        # Start Flask app in main thread
        logger.info("Starting Flask web interface on port 5000...")
        run_flask_app()
        
    except KeyboardInterrupt:
        logger.info("Shutdown requested by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)