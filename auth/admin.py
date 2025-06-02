from sqlmodel import Session
from passlib.context import CryptContext
from ..models.AdminUser import Admin
from ..database import engine

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to hash password


def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Function to create an admin user


def create_admin(username: str, password: str):
    with Session(engine) as session:
        hashed_pw = hash_password(password)
        admin = Admin(username=username, hashed_password=hashed_pw)
        session.add(admin)
        session.commit()
        session.refresh(admin)
