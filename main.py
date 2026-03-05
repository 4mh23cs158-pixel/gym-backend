from fastapi import FastAPI
from routes.user_routes import router as user_router
from routes.meal_routes import router as meal_router
from routes.workout_routes import router as workout_router
from routes.goal_routes import router as goal_router
from db import get_db,DATABASE_URL
from sqlalchemy import create_engine
from models import Base
app = FastAPI()


app.include_router(user_router)
app.include_router(meal_router)
app.include_router(workout_router)
app.include_router(goal_router)

#to create database

engine=create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

@app.get("/")
def read_root():
    return {"Hello": "World"}







if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)