import os
import jwt
import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def create_access_token(user):
    encode = {
        "user_id": user.id,
        "username": user.username,
        "role": user.role,
        "exp": datetime.datetime.now() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])