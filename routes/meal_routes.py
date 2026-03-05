from fastapi import APIRouter, Depends, HTTPException
from models import Meal
from db import get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from utils.auth import get_current_user
from models import User
from utils.nutrition import get_nutrition, search_food

class MealBase(BaseModel):
    name: str
    calories: float
    protein: float
    carbs: float
    fat: float

class MealCreate(BaseModel):
    meal_name: str
    quantity: float = 100.0
    unit: str = "grams"

class MealUpdate(BaseModel):
    name: str
    calories: float
    protein: float
    carbs: float
    fat: float

class MealResponse(MealBase):
    id: int
    user_id: int
    created_at: datetime
    class Config:
        orm_mode = True

class MealRouter(APIRouter):
    def __init__(self):
        super().__init__(tags=["meals"])
        self.add_api_route("/meals/search", self.search_meals, methods=["GET"])
        self.add_api_route("/meals", self.get_all_meals, methods=["GET"])
        self.add_api_route("/meals/{meal_id}", self.get_meal, methods=["GET"])
        self.add_api_route("/meals", self.add_meal_auto, methods=["POST"])
        self.add_api_route("/meals/{meal_id}", self.update_meal, methods=["PUT"])
        self.add_api_route("/meals/{meal_id}", self.delete_meal, methods=["DELETE"])

    def search_meals(self, q: str):
        if not q:
            return []
        return search_food(q)

    def get_all_meals(self, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
        return db.query(Meal).filter(Meal.user_id == current_user.id).order_by(Meal.created_at.desc()).all()

    def get_meal(self, meal_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
        meal = db.query(Meal).filter(Meal.id == meal_id, Meal.user_id == current_user.id).first()
        if not meal:
            raise HTTPException(status_code=404, detail="Meal not found")
        return meal

    def add_meal_auto(self, meal: MealCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
        nutrition = get_nutrition(meal.meal_name, quantity=meal.quantity, unit=meal.unit)
        db_meal = Meal(
            name=f"{meal.meal_name} ({meal.quantity} {meal.unit})",
            calories=nutrition["calories"],
            protein=nutrition["protein"],
            carbs=nutrition["carbs"],
            fat=nutrition["fat"],
            user_id=current_user.id
        )
        db.add(db_meal)
        db.commit()
        db.refresh(db_meal)
        return db_meal

    def update_meal(self, meal_id: int, meal: MealUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
        meal_to_update = db.query(Meal).filter(Meal.id == meal_id, Meal.user_id == current_user.id).first()
        if not meal_to_update:
            raise HTTPException(status_code=404, detail="Meal not found")
        meal_to_update.name = meal.name
        meal_to_update.calories = meal.calories
        meal_to_update.protein = meal.protein
        meal_to_update.carbs = meal.carbs
        meal_to_update.fat = meal.fat
        db.commit()
        return meal_to_update

    def delete_meal(self, meal_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
        meal_to_delete = db.query(Meal).filter(Meal.id == meal_id, Meal.user_id == current_user.id).first()
        if not meal_to_delete:
            raise HTTPException(status_code=404, detail="Meal not found")
        db.delete(meal_to_delete)
        db.commit()
        return {"message": "Meal deleted successfully"}

router = MealRouter()