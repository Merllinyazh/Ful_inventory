from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config import SessionLocal
from routes.auth import get_current_user
from services.auditservices import AuditService

router = APIRouter(prefix="/audit", tags=["Audit Logs"])


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_logs(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return AuditService.get_logs(db)


@router.get("/user/{user_id}")
def get_user_logs(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return AuditService.get_user_logs(user_id, db)