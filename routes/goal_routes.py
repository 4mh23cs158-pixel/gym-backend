from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import get_db
from schemas.goal_schemas import GoalCreate
from repositories.goal_repo import create_goal, get_goal
from utils.auth import get_current_user
from models import User


router = APIRouter(prefix="/goals", tags=["Goals"])

@router.post("/")
def add_goal(goal: GoalCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_goal(db, goal, current_user.id)

@router.get("/")
def list_goals(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_goal(db, current_user.id)