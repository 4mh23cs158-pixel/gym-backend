from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import get_db
from schemas.workout_schemas import WorkoutCreate
from repositories.workout_repo import create_workout, get_user_workouts, delete_workout


from utils.auth import get_current_user
from models import User

router = APIRouter(prefix="/workouts", tags=["Workouts"])

@router.post("/")
def add_workout(workout: WorkoutCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_workout(db, workout, current_user.id)

@router.get("/")
def list_workouts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_user_workouts(db, current_user.id)

@router.delete("/{workout_id}")
def remove_workout(workout_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return delete_workout(db, workout_id, current_user.id)