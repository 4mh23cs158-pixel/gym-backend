from pydantic import BaseModel
from datetime import datetime

class WorkoutCreate(BaseModel):
    exercise_name: str
    sets: int
    reps: int
    weight: int


class WorkoutResponse(BaseModel):
    id: int
    exercise_name: str
    sets: int
    reps: int
    weight: int
    created_at: datetime

    class Config:
        orm_mode = True