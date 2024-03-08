#!/usr/bin/python3
"""It creates a BaseModel class that inherits from BaseModel"""
from models.engine.file_storage import FileStorage

# Replace with your specific file storage configuration
storage = FileStorage()  # Example instantiation
storage.reload()