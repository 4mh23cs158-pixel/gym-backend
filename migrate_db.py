from sqlalchemy import text
from db import engine

def log(msg):
    print(msg)
    with open("migration.log", "a") as f:
        f.write(msg + "\n")

def migrate():
    with open("migration.log", "w") as f:
        f.write("Starting migration...\n")
    try:
        with engine.connect() as conn:
            log("Connected to database. Running migration...")
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
            log("Migration successful: 'goals' table updated.")
    except Exception as e:
        log(f"Migration failed: {e}")

if __name__ == "__main__":
    migrate()
