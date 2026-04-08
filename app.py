from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import jwt  # PyJWT
from datetime import datetime, timedelta

app = FastAPI()

# --- Конфигурация RSA ---
# В реальном проекте загружайте ключи из .pem файлов или переменных окружения
PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY----- ... -----END RSA PRIVATE KEY-----"""
PUBLIC_KEY = """-----BEGIN PUBLIC KEY----- ... -----END PUBLIC KEY-----"""
ALGORITHM = "RS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# --- Логика ACL ---
def check_permissions(required_role: str):
    def role_checker(token: str = Depends(oauth2_scheme)):
        try:
            payload = jwt.decode(token, PUBLIC_KEY, algorithms=[ALGORITHM])
            user_role = payload.get("role")
            if user_role != required_role:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied: insufficient permissions"
                )
            return payload
        except jwt.PyJWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

    return role_checker


# --- Эндпоинты ---
@app.get("/")
def read_root():
    return {"message": "FastAPI Secure API"}


@app.get("/admin-data", dependencies=[Depends(check_permissions("admin"))])
async def get_admin_data():
    return {"status": "Welcome, Admin. This is secure data."}


@app.get("/user-data", dependencies=[Depends(check_permissions("user"))])
async def get_user_data():
    return {"status": "Hello User!"}
