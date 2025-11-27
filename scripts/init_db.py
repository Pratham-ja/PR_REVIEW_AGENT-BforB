#!/usr/bin/env python3
"""
Database initialization script
"""
import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from repositories.database import db_manager
from config import settings


async def init_database():
    """Initialize the database with tables"""
    print(f"Initializing database: {settings.database_url}")
    
    try:
        # Initialize the database manager
        db_manager.initialize()
        
        # Create all tables
        await db_manager.create_tables()
        
        print("✓ Database tables created successfully")
        
    except Exception as e:
        print(f"✗ Error initializing database: {e}")
        return False
    
    finally:
        await db_manager.close()
    
    return True


async def drop_database():
    """Drop all database tables (for testing/reset)"""
    print(f"Dropping all tables from: {settings.database_url}")
    
    try:
        # Initialize the database manager
        db_manager.initialize()
        
        # Drop all tables
        await db_manager.drop_tables()
        
        print("✓ Database tables dropped successfully")
        
    except Exception as e:
        print(f"✗ Error dropping database: {e}")
        return False
    
    finally:
        await db_manager.close()
    
    return True


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Database management script")
    parser.add_argument(
        "action", 
        choices=["init", "drop", "reset"],
        help="Action to perform: init (create tables), drop (drop tables), reset (drop then create)"
    )
    
    args = parser.parse_args()
    
    if args.action == "init":
        success = asyncio.run(init_database())
    elif args.action == "drop":
        success = asyncio.run(drop_database())
    elif args.action == "reset":
        print("Resetting database (drop + init)...")
        success = asyncio.run(drop_database())
        if success:
            success = asyncio.run(init_database())
    
    sys.exit(0 if success else 1)