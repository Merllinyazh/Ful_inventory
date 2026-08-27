from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config import SessionLocal
from routes.auth import admin_required
from services.movementservices import MovementService, MovementCreate

router = APIRouter(prefix="/movement", tags=["Movement"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_movement(
    data: MovementCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(admin_required)
):
    return MovementService.create_movement(data, current_user, db)