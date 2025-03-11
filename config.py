import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    CLOUD_NAME = os.getenv('CLOUD_NAME')
    API_KEY = os.getenv("API_KEY")
    API_SECRET = os.getenv("API_SECRET")
