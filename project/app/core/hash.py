import hashlib
import base64

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def _pre_hash(password: str) -> str:
    return base64.b64encode(hashlib.sha256(password.encode()).digest()).decode()


def hash_password(password: str) -> str:
    pre_hashed = base64.b64encode(hashlib.sha256(password.encode()).digest()).decode()
    return pwd_context.hash(pre_hashed)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(_pre_hash(plain_password), hashed_password)