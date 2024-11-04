import os
from dotenv import load_dotenv

load_dotenv()

print("System DATABASE_URI:", os.environ.get('DATABASE_URI'))