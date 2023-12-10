import os
from jwt import encode, decode

# Obtener la clave desde una variable de entorno
SECRET_KEY = os.getenv("JWT_SECRET_KEY")

def create_token(data: dict) -> str:
    token: str = encode(payload=data, key=str(SECRET_KEY), algorithm="HS256")
    return token

def validate_token(token: str) -> dict:
    data: dict = decode(token, key=str(SECRET_KEY), algorithms=['HS256'])
    return data