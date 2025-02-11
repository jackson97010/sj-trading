# login_test.py
import os
from dotenv import load_dotenv
import shioaji as sj
from pathlib import Path

def show_version() -> str:
    print(f"Shioaji Version: {sj.__version__}")
    return sj.__version__

def login():
    env_path = Path(__file__).parent / ".env"
    loaded = load_dotenv(dotenv_path=env_path)
    
    if not loaded:
        print("The .env file was not loaded. Check the file path.")
        return None
    
    api = sj.Shioaji(simulation=True)
    accounts = api.login(
        api_key=os.getenv("API_KEY"),
        secret_key=os.getenv("API_SECRET"),
    )
    api.activate_ca(
        ca_path=os.getenv("CA_PATH"),
        ca_passwd=os.getenv("CA_PASSWORD"),
        person_id=os.getenv("PERSON_ID"),
    )
    print(f"Available accounts: {accounts}")
    return api  # Return the api object

if __name__ == "__main__":
    login()
