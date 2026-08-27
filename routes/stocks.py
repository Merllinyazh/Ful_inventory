from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config import SessionLocal
from routes.auth import get_current_user
from services.stockservices import StockService

router = APIRouter(prefix="/stock", tags=["Stock"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_stock(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return StockService.get_all_stock(db)


@router.get("/location/{location_id}")
def get_location_stock(
    location_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return StockService.get_stock_by_location(location_id, db)