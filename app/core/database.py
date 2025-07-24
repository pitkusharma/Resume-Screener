import motor.motor_asyncio
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Create the Motor client
db_client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGO_URI"))

# Get the database
db = db_client[os.getenv("DB_NAME")]

# Collections
resumes_collection = db["resumes"]
