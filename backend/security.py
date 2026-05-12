"""
MDIP FastAPI Backend - Security & JWT Utilities
Handles JWT token generation, validation, and password hashing
"""

from datetime import datetime, timedelta
from typing import Optional
import jwt
from passlib.context import CryptContext
from pydantic import BaseModel
import os

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class TokenData(BaseModel):
    """Token payload data"""
    user_id: str
    email: str
    exp: Optional[datetime] = None


class Token(BaseModel):
    """Token response model"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against a hashed password
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: Hashed password from database
        
    Returns:
        True if passwords match, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_id: str, email: str, expires_delta: Optional[timedelta] = None) -> Token:
    """
    Create a JWT access token
    
    Args:
        user_id: User's unique identifier
        email: User's email
        expires_delta: Custom expiration time
        
    Returns:
        Token object with access_token and expiration
    """
    if expires_delta is None:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    expire = datetime.utcnow() + expires_delta
    
    to_encode = {
        "user_id": user_id,
        "email": email,
        "exp": expire
    }
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return Token(
        access_token=encoded_jwt,
        token_type="bearer",
        expires_in=int(expires_delta.total_seconds())
    )


def verify_token(token: str) -> Optional[TokenData]:
    """
    Verify and decode a JWT token
    
    Args:
        token: JWT token string
        
    Returns:
        TokenData if valid, None if invalid or expired
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        email: str = payload.get("email")
        
        if user_id is None or email is None:
            return None
            
        return TokenData(user_id=user_id, email=email)
    except jwt.ExpiredSignatureError:
        print("Token expired")
        return None
    except jwt.InvalidTokenError:
        print("Invalid token")
        return None


def decode_token(token: str) -> Optional[dict]:
    """
    Decode a JWT token without verification (use with caution)
    
    Args:
        token: JWT token string
        
    Returns:
        Decoded payload dictionary
    """
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.InvalidTokenError:
        return None