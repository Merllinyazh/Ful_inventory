import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from config import SessionLocal, verify_token
from services.authservices import AuthService, RegisterUser, LoginUser

router = APIRouter(prefix="/auth", tags=["Authentication"])

security = HTTPBearer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        return verify_token(credentials.credentials)

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.post("/register", status_code=201)
def register(data: RegisterUser, db: Session = Depends(get_db)):
    return AuthService.register_user(data, db)


@router.post("/login")
def login(data: LoginUser, db: Session = Depends(get_db)):
    return AuthService.login_user(data, db)


@router.get("/protected")
def protected(current_user: dict = Depends(get_current_user)):
    return {
        "message": f"Welcome back, {current_user['username']}!",
        "user": current_user
    }