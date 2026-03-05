from sqlalchemy import text
from db import engine

with engine.connect() as conn:
    conn.execute(text("""
        ALTER TABLE goals
        DROP COLUMN IF EXISTS name,
        DROP COLUMN IF EXISTS calories,
        DROP COLUMN IF EXISTS protein,
        DROP COLUMN IF EXISTS carbs,
        DROP COLUMN IF EXISTS fat,
        ADD COLUMN IF NOT EXISTS calorie_goal INTEGER,
        ADD COLUMN IF NOT EXISTS protein_goal INTEGER,
        ADD COLUMN IF NOT EXISTS workout_goal INTEGER;
    """))
    conn.commit()
    print("Migration done! goals table updated.")
