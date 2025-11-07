"""
Configuration management for Jerdon AI backend.
All configuration values loaded from environment variables.
"""
import os
from dotenv import load_dotenv
from typing import Dict, List

load_dotenv()

# Environment
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
IS_PRODUCTION = ENVIRONMENT == "production"
APP_VERSION = "1.0.0"

# Google Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

# MongoDB Configuration
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "jerdon_ai_dev")

# Firebase Configuration
FIREBASE_APP_ID = os.getenv("FIREBASE_APP_ID", "")
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "./serviceAccountKey.json")

# CORS Configuration
ALLOWED_ORIGINS_STR = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000")
CORS_ORIGINS: List[str] = [origin.strip() for origin in ALLOWED_ORIGINS_STR.split(",")]

# Redis Configuration
REDIS_ENABLED = os.getenv("REDIS_ENABLED", "false").lower() == "true"
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# Security
ADMIN_API_KEY = os.getenv("ADMIN_API_KEY", "change_this_in_production")

# File Upload Limits
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
MAX_FILE_SIZE = MAX_FILE_SIZE_MB * 1024 * 1024

# Query Limits
MAX_QUERY_LENGTH = int(os.getenv("MAX_QUERY_LENGTH", "10000"))

# Rate Limiting
RATE_LIMIT_ENABLED = os.getenv("RATE_LIMIT_ENABLED", "true").lower() == "true"

# Frontend URL
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

# Allowed file MIME types
ALLOWED_MIME_TYPES = [
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
]

# Plan Limits
PLAN_LIMITS: Dict[str, int] = {
    "Trial": 25,
    "Starter": 150,
    "Professional": 2000,
    "Enterprise": 20000
}

# Document Limits per Plan
PLAN_DOC_LIMITS: Dict[str, int] = {
    "Trial": 3,
    "Starter": 15,
    "Professional": 200,
    "Enterprise": -1
}

# File Size Limits per Plan (in MB)
PLAN_FILE_SIZE_LIMITS: Dict[str, int] = {
    "Trial": 10,
    "Starter": 25,
    "Professional": 100,
    "Enterprise": 500
}

# Pricing Information
PLAN_PRICING = {
    "Trial": {
        "monthly": 0,
        "yearly": 0,
        "duration_days": 7,
        "stripe_monthly": None,
        "stripe_yearly": None,
        "display_price": "Free",
        "description": "7-day free trial"
    },
    "Starter": {
        "monthly": 19,
        "yearly": 190,
        "stripe_monthly": "price_starter_monthly",
        "stripe_yearly": "price_starter_yearly",
        "display_price": "$19",
        "description": "For individuals and small teams"
    },
    "Professional": {
        "monthly": 149,
        "yearly": 1490,
        "stripe_monthly": "price_pro_monthly",
        "stripe_yearly": "price_pro_yearly",
        "display_price": "$149",
        "description": "For growing businesses"
    },
    "Enterprise": {
        "monthly": 999,
        "yearly": 9990,
        "stripe_monthly": "price_enterprise_monthly",
        "stripe_yearly": "price_enterprise_yearly",
        "display_price": "$999",
        "description": "For large organizations",
        "custom": True
    }
}

print(f"✅ Configuration loaded for {ENVIRONMENT} environment")
