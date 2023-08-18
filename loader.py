from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.getenv("API_TOKEN")
ALIEXPRESS_API_KEY = os.getenv("ALIEXPRESS_API_KEY")
username=os.getenv("username")
password=os.getenv("password")