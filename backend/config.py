"""
MDIP Backend Configuration Module
Centralized environment variable management for all services
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ============================================================================
# JWT Configuration
# ============================================================================
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# ============================================================================
# Stripe Configuration
# ============================================================================
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY", "")

# Stripe Product Configuration
STRIPE_MONTHLY_PRODUCT_ID = os.getenv("STRIPE_MONTHLY_PRODUCT_ID", "prod_mdip_monthly")
STRIPE_ANNUAL_PRODUCT_ID = os.getenv("STRIPE_ANNUAL_PRODUCT_ID", "prod_mdip_annual")

# Stripe URLs
STRIPE_SUCCESS_URL = os.getenv(
    "STRIPE_SUCCESS_URL",
    "http://localhost:3000/dashboard/billing/success"
)
STRIPE_CANCEL_URL = os.getenv(
    "STRIPE_CANCEL_URL",
    "http://localhost:3000/dashboard/billing/cancel"
)

# ============================================================================
# API Configuration
# ============================================================================
API_V1_PREFIX = "/api/v1"
API_TITLE = "MDIP Backend API"
API_VERSION = "1.0.0"

# ============================================================================
# CORS Configuration
# ============================================================================
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,http://localhost:8080"
).split(",")

# ============================================================================
# Database Configuration (For Future Use)
# ============================================================================
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./mdip.db")

# ============================================================================
# Logging Configuration
# ============================================================================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
