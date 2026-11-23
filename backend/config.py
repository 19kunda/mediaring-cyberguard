import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Read the secret key without hardcoding it
SECRET_KEY = os.getenv("SECRET_KEY")

# Stop the application if the secret key is missing
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is missing from the .env file.")