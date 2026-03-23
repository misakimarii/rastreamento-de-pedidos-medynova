import os
from dotenv import load_dotenv

load_dotenv()

AMPLA_TOKEN = os.getenv("AMPLA_TOKEN")
AMPLA_USER = os.getenv("AMPLA_USER")   
AMPLA_SENHA = os.getenv("AMPLA_SENHA")
BASE_URL= os.getenv("BASE_URL")