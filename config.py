"""
Configuration module for environment variables.

This module loads environment variables using `dotenv` and provides constants
for key configurations used throughout the project.

Environment Variables:
    BASE_URL (str): The base URL for scraping or API requests.
    DATABASE_URL (str): The database connection string.

Usage:
    Import the constants defined here to access configuration values:
        from config import BASE_URL, DATABASE_URL
"""

import os

from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Base URL for scraping
BASE_URL = os.getenv("BASE_URL")

# Database connection string
DATABASE_URL = os.getenv("DATABASE_URL")
