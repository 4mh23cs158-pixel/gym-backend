import os
import bcrypt
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from dotenv import load_dotenv

load_dotenv()

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

def verify_password(plain_password: str, hashed_password: str):
    """Verify a plain password against a hashed password."""
    password_bytes = plain_password.encode('utf-8')
    # bcrypt 4.x has a 72-byte limit; truncate to avoid ValueError
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    return bcrypt.checkpw(password_bytes, hashed_password.encode('utf-8'))

def get_password_hash(password: str):
    """Hash a password using bcrypt."""
    password_bytes = password.encode('utf-8')
    # bcrypt 4.x has a 72-byte limit; truncate to avoid ValueError
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt).decode('utf-8')


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
