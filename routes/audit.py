from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config import SessionLocal
from routes.auth import admin_required
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
    current_user: dict = Depends(admin_required)
):
    return AuditService.get_logs(db)

