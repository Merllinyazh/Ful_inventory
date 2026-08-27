from fastapi import HTTPException
from pydantic import BaseModel
from config import create_access_token
from models.database import User
from services.auditservices import AuditService


class RegisterUser(BaseModel):
    username: str
    email: str
    password: str
    role: str


class LoginUser(BaseModel):
    email: str
    password: str


class AuthService:

    @staticmethod
    def register_user(data, db):

        if db.query(User).filter(User.email == data.email).first():
            raise HTTPException(
                status_code=409,
                detail="Email already registered"
            )

        user = User(
            username=data.username,
            email=data.email,
            password=data.password,
            role=data.role
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        # Audit log
        AuditService.create_log(
            user_id=user.id,
            action="REGISTER",
            details=f"User {user.username} registered",
            db=db
        )

        return {
            "message": "User registered successfully",
            "user": user.to_dict()
        }


    @staticmethod
    def login_user(data, db):

        user = db.query(User).filter(
            User.email == data.email,
            User.password == data.password
        ).first()

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        # Audit log
        AuditService.create_log(
            user_id=user.id,
            action="LOGIN",
            details=f"User {user.username} logged in",
            db=db
        )

        token = create_access_token(user)

        return {
            "message": "Login successful",
            "access_token": token,
            "token_type": "Bearer"
        }