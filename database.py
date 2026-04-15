from cryptography.fernet import Fernet
from dotenv import load_dotenv
from supabase import create_client
import os

load_dotenv()

URL = os.getenv("URL")
KEY = os.getenv("KEY")
FERNET_KEY = os.getenv("FERNET_KEY").encode()

supabase = create_client(URL, KEY)

fernet = Fernet(FERNET_KEY)

def encrypt_password(password):
    return fernet.encrypt(password.encode()).decode()

def decrypt_password(password):
    return fernet.decrypt(password.encode()).decode()