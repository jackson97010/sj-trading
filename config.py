'''
This is used to confirm that the .env file is loaded correctly.
'''
import os
from dotenv import load_dotenv
from pathlib import Path

# Construct the path to the .env file relative to this file's location
env_path = Path(__file__).parent / ".env"
loaded = load_dotenv(dotenv_path=env_path)

if not loaded:
    print("The .env file was not loaded. Check the file path.")
else:
    print("The .env file was loaded successfully!")
    print("API_KEY:", os.getenv("API_KEY"))
    print("API_SECRET:", os.getenv("API_SECRET"))
