import bcrypt
from src.config import auth_pwd, settings
from typing import Optional
from datetime import timedelta, datetime
import jwt
from src.shared.dto.auth_dto import TokenDataDTO
from fastapi.exceptions import HTTPException
from fastapi import Depends, status
from src.core.domain.enums.roles import UserRole


def get_pwd_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def create_access_token(data: dict, expires_delta: Optional[timedelta]=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=150)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

'''verify jwt'''
# def verify_token(token: str = Depends(auth_pwd.oauth2_schema)) -> TokenData:
#     try:
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
#         user_id: str = payload.get("sub")
        
#         if user_id is None:
#             raise HTTPException(status_code=401, detail="Неполный токен")
            
#         return TokenData(user_id=int(user_id))
#     except (jwt.PyJWTError, ValueError):
#         raise HTTPException(status_code=401, detail="Ошибка авторизации")

'''проверка пользователья по ролья в системе испльзоуя полезные данные из jwt'''

def verify_token(token: str = Depends(auth_pwd.oauth2_schema)) -> TokenDataDTO:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        role: str = payload.get("role")
        if user_id is None or role is None:
            raise HTTPException(status_code=401, detail="Неполный токен")
            
        return TokenDataDTO(user_id=int(user_id), user_role=role)

    except jwt.PyJWTError as e:
        raise HTTPException(status_code=401, detail="Ошибка авторизации: " + str(e))
    except ValueError as e:
        raise HTTPException(status_code=401, detail="Ошибка формата данных")