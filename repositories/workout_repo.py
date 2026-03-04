from sqlalchemy.orm import Session
from models import Workout


def create_workout(db: Session, workout, user_id: int):
    new_workout = Workout(
        exercise_name=workout.exercise_name,
        sets=workout.sets,
        reps=workout.reps,
        weight=workout.weight,
        user_id=user_id
    )

    db.add(new_workout)
    db.commit()
    db.refresh(new_workout)

    return new_workout


def get_user_workouts(db: Session, user_id: int):
    return db.query(Workout).filter(Workout.user_id == user_id).all()


def delete_workout(db: Session, workout_id: int, user_id: int):

    workout = db.query(Workout).filter(
        Workout.id == workout_id,
        Workout.user_id == user_id
    ).first()

    if workout:
        db.delete(workout)
        db.commit()

    return workout