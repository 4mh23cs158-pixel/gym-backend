from fastapi import APIRouter
from models import Meal
from db import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List
from pydantic import BaseModel
from datetime import datetime
from fastapi import Depends
from utils.nutrition import get_nutrition

class MealBase(BaseModel):
    name: str
    calories: int
    protein: int
    carbs: int
    fat: int

class MealCreate(MealBase):
    pass

class MealUpdate(BaseModel):
    name: str
    calories: int
    protein: int
    carbs: int
    fat: int

class MealResponse(MealBase):
    id: int
    user_id: int
    created_at: datetime
    class Config:
        orm_mode = True

class MealRouter(APIRouter):
    def __init__(self):
        super().__init__(tags=["meals"])
        self.add_api_route("/meals", self.get_all_meals, methods=["GET"])
        self.add_api_route("/meals/{meal_id}", self.get_meal, methods=["GET"])
        self.add_api_route("/meals/{meal_id}", self.update_meal, methods=["PUT"])
        self.add_api_route("/meals/{meal_id}", self.delete_meal, methods=["DELETE"])



    def get_all_meals(self, db: Session = Depends(get_db)):
        return db.query(Meal).all()

    def get_meal(self, meal_id: int, db: Session = Depends(get_db)):
        meal = db.query(Meal).filter(Meal.id == meal_id).first()
        if not meal:
            raise HTTPException(status_code=404, detail="Meal not found")
        return meal

    def update_meal(self, meal_id: int, meal: MealUpdate, db: Session = Depends(get_db)):
        meal_to_update = db.query(Meal).filter(Meal.id == meal_id).first()
        if not meal_to_update:
            raise HTTPException(status_code=404, detail="Meal not found")
        meal_to_update.name = meal.name
        meal_to_update.calories = meal.calories
        meal_to_update.protein = meal.protein
        meal_to_update.carbs = meal.carbs
        meal_to_update.fat = meal.fat
        db.commit()
        return meal_to_update

    def delete_meal(self, meal_id: int, db: Session = Depends(get_db)):
        meal_to_delete = db.query(Meal).filter(Meal.id == meal_id).first()
        if not meal_to_delete:
            raise HTTPException(status_code=404, detail="Meal not found")
        db.delete(meal_to_delete)
        db.commit()
        return {"message": "Meal deleted successfully"}

router = MealRouter()

@router.post("/meals")
def add_meal(name: str, db: Session = Depends(get_db)):

    nutrition = get_nutrition(name)

    meal = Meal(
        name=name,
        calories=nutrition["calories"],
        protein=nutrition["protein"],
        carbs=nutrition["carbs"]
    )

    db.add(meal)
    db.commit()
    db.refresh(meal)

    return meal