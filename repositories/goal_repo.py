from sqlalchemy.orm import Session
from models import Goal


def create_goal(db: Session, goal, user_id: int):

    new_goal = Goal(
        calorie_goal=goal.calorie_goal,
        protein_goal=goal.protein_goal,
        workout_goal=goal.workout_goal,
        user_id=user_id
    )

    db.add(new_goal)
    db.commit()
    db.refresh(new_goal)

    return new_goal


def get_goal(db: Session, user_id: int):

    return db.query(Goal).filter(Goal.user_id == user_id).first()