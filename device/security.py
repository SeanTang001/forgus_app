import hashlib
import cryptography
from cryptography.fernet import Fernet
import json

def encrypt(key, payload):
    print(key)
    print(payload)
    return Fernet(key.encode()).encrypt(payload.encode()).decode()

def decrypt(key, payload):
    print(key)
    return Fernet(key.encode()).decrypt(payload.encode()).decode()

def genkey():
    return(Fernet.generate_key().decode())
