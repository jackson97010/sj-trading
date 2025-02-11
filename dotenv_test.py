'''
2025.02.10 v1.0.0
-----------------
This scripts is used to test the dotenv package. 
It will load the .env file and print the API_KEY and API_SECRET values.
'''


import os
from dotenv import load_dotenv

# Explicitly specify the path to ensure we're loading the correct file
from pathlib import Path
env_path = Path(__file__).parent / ".env"
loaded = load_dotenv(dotenv_path=env_path)

if not loaded:
    print("The .env file was not loaded. Check the file path.")
else:
    print("The .env file was loaded successfully!")
    print("API_KEY:", os.getenv("API_KEY"))
    print("API_SECRET:", os.getenv("API_SECRET"))
