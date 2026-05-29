from src.core.domain.services.auth_service import AuthService
from src.infrastructure.security.auth import get_pwd_hash, create_access_token

class JWTAuthService(AuthService):
    def get_password_hash(self, password: str) -> str:
        return get_pwd_hash(password)

    def create_access_token(self, data: dict) -> str:
        return create_access_token(data=data)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        from src.infrastructure.security.auth import verify_password
        return verify_password(plain_password, hashed_password)


def get_auth_service() -> AuthService:
    return JWTAuthService()