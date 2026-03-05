from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db import get_db
from models import User
from repositories.user_repo import UserRepo
from schemas.user_schemas import UserSchema
from schemas.Token_schemas import Token, LoginRequest
from utils.auth import get_password_hash, verify_password, create_access_token, get_current_user

router = APIRouter()


@router.post("/signup")
def signup(user: UserSchema, db: Session = Depends(get_db)):
    user_repo = UserRepo(db)
    # Check if user already exists
    existing_user = user_repo.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    # Hash the password before saving
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    user_repo.add_user(db_user)
    return {"message": "User signed up successfully"}


@router.post("/login", response_model=Token)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate user and return access token."""
    user_repo = UserRepo(db)
    user = user_repo.get_user_by_email(credentials.email)
    
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
def logout():
    return {"message": "User logged out successfully"}

@router.get("/users/me", response_model=UserSchema)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
