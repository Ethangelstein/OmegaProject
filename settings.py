from os import getenv
from dotenv import load_dotenv

load_dotenv()

# Flask
FLASK_SECRET_KEY = getenv("FLASK_SECRET_KEY")

# Database
DATABASE_HOST = getenv("DATABASE_HOST")
DATABASE_PASSWORD = getenv("DATABASE_PASSWORD")
DATABASE_USER = getenv("DATABASE_USER")
DATABASE = getenv("DATABASE")
