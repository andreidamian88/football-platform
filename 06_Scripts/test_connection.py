import os
import psycopg2

from pathlib import Path
from dotenv import load_dotenv

# Find the project root
project_root = Path(__file__).resolve().parent.parent

# Load .env from the project root
env_path = project_root / ".env"

load_dotenv(dotenv_path=env_path)

# Check whether the password was loaded (without displaying it)
password = os.getenv("DB_PASSWORD")

if not password:
    print("ERROR: DB_PASSWORD was not loaded.")
    print("Expected .env location:", env_path)
    raise SystemExit(1)

print("Environment variables loaded successfully.")

try:
    connection = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=password
    )

    print("Successfully connected to PostgreSQL!")

    connection.close()

except psycopg2.Error as error:
    print("Database connection failed:", error)