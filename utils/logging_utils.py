"""Logging utilities for bot activities"""

import logging
from datetime import datetime
from app import app, db
from models import BotLog, Server

def log_command_usage(user_id: str, server_id: str, command: str, details: str = ""):
    """Log command usage to database"""
    
    with app.app_context():
        try:
            # Create log entry
            log_entry = BotLog(
                server_id=server_id,
                user_id=user_id,
                username="User",
                command=command,
                channel_id="0",
                details=details
            )
            
            db.session.add(log_entry)
            db.session.commit()
            
        except Exception as e:
            logging.error(f"Error logging command usage: {e}")

def get_recent_logs(guild_id: str, limit: int = 50):
    """Get recent logs for a guild"""
    with app.app_context():
        server = Server.query.filter_by(guild_id=guild_id).first()
        if not server:
            return []
        
        logs = BotLog.query.filter_by(server_id=server.id).order_by(BotLog.timestamp.desc()).limit(limit).all()
        return logs
