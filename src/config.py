from dotenv import load_dotenv
import os

load_dotenv()

MODE = os.environ.get("MODE")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

REDIS_HOST = os.environ.get("REDIS_HOST")

GO_USER = os.environ.get("GOOGLE_USER")
GO_PASS = os.environ.get("GOOGLE_PASS")
