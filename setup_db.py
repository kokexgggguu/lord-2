#!/usr/bin/env python3
"""Database setup script"""

from app import app, db
from models import Server, Match, MatchReminder, BotLog

def setup_database():
    """Create all database tables"""
    with app.app_context():
        # Drop all tables and recreate
        db.drop_all()
        db.create_all()
        print("Database tables created successfully!")
        
        # Verify tables exist
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"Created tables: {tables}")

if __name__ == "__main__":
    setup_database()