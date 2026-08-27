from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config import SessionLocal
from routes.auth import get_current_user, admin_required
from services.productservices import ProductService, ProductCreate

router = APIRouter(prefix="/products", tags=["Products"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", status_code=201)
def create_product(
    data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(admin_required)
):
    return ProductService.create_product(data, current_user, db)


@router.get("/")
def get_products(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return ProductService.get_products(db)


@router.get("/{product_id}")
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return ProductService.get_product(product_id, db)


@router.put("/{product_id}")
def update_product(
    product_id: int,
    data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(admin_required)
):
    return ProductService.update_product(product_id, data, db)


@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(admin_required)
):
    return ProductService.delete_product(product_id, db)