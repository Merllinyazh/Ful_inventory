from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config import SessionLocal
from routes.auth import get_current_user
from services.movementservices import MovementService, MovementCreate

router = APIRouter(prefix="/movements", tags=["Movements"])


def get_db():

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("/", status_code=201)
def create_movement(
    data: MovementCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    return MovementService.create_movement(data, current_user, db)


@router.get("/")
def get_movements(db: Session = Depends(get_db)):

    return MovementService.get_movements(db)