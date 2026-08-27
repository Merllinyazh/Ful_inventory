from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config import SessionLocal
from services.stockservices import StockService, StockCreate
from routes.auth import get_current_user

router = APIRouter(prefix="/stocks", tags=["Stock Management"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def add_stock(
    data: StockCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return StockService.add_stock(data, db)


@router.get("/")
def get_stocks(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return StockService.get_stocks(db)


@router.get("/{product_id}/{location_id}")
def get_stock(
    product_id: int,
    location_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return StockService.get_stock(product_id, location_id, db)