from pydantic import BaseModel


class GoalCreate(BaseModel):
    calorie_goal: int
    protein_goal: int
    workout_goal: int


class GoalResponse(BaseModel):

    id: int
    calorie_goal: int
    protein_goal: int
    workout_goal: int

    class Config:
        orm_mode = True