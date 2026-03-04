from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import get_db
from schemas.workout_schemas import WorkoutCreate
from repositories.workout_repo import create_workout, get_user_workouts, delete_workout


router = APIRouter(prefix="/workouts", tags=["Workouts"])

@router.post("/")
def add_workout(workout: WorkoutCreate, user_id: int, db: Session = Depends(get_db)):
    return create_workout(db, workout, user_id)

@router.get("/")
def list_workouts(user_id: int, db: Session = Depends(get_db)):
    return get_user_workouts(db, user_id)

@router.delete("/{workout_id}")
def remove_workout(workout_id: int, user_id: int, db: Session = Depends(get_db)):
    return delete_workout(db, workout_id, user_id)