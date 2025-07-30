import os
from dotenv import load_dotenv

load_dotenv() 

DATABASE_URL = "postgresql+asyncpg://postgres:1234@localhost:5432/currency"