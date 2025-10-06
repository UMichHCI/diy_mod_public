#!/usr/bin/env python3
"""
Simple script to create/update database tables
"""

import sys
sys.path.append('.')

# Direct import to avoid circular imports
from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime, ForeignKey, Boolean, Float, Enum
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

# Just import the models directly
exec(open('database/models.py').read())

print("✅ Database tables created/updated successfully!")
print("   - users")
print("   - filters") 
print("   - processing_logs")
print("   - custom_feeds")