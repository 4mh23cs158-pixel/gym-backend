from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import get_db
from schemas.goal_schemas import GoalCreate
from repositories.goal_repo import create_goal, get_goal
from utils.auth import get_current_user


router = APIRouter(prefix="/goals", tags=["Goals"])

@router.post("/")
def add_goal(goal: GoalCreate, user_id: int, db: Session = Depends(get_db)):
    return create_goal(db, goal, user_id)

@router.get("/")
def list_goals(user_id: int, db: Session = Depends(get_db)):
    return get_goal(db, user_id)