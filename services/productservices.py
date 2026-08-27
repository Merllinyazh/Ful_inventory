from fastapi import HTTPException
from pydantic import BaseModel
from models.database import Product
from services.auditservices import AuditService


class ProductCreate(BaseModel):
    name: str
    sku: str
    price: float
    quantity: int = 0


class ProductService:

    @staticmethod
    def create_product(data, current_user, db):
        if db.query(Product).filter(Product.sku == data.sku).first():
            raise HTTPException(status_code=409, detail="SKU already exists")

        product = Product(
            name=data.name,
            sku=data.sku,
            price=data.price,
            quantity=data.quantity
        )

        db.add(product)
        db.commit()
        db.refresh(product)

        AuditService.create_log(
            current_user["user_id"],
            "CREATE_PRODUCT",
            f"Product '{product.name}' created",
            db
        )

        return {
            "message": "Product created successfully",
            "product": product.to_dict()
        }


    @staticmethod
    def get_products(db):
        products = db.query(Product).all()
        return [product.to_dict() for product in products]


    @staticmethod
    def get_product(product_id, db):
        product = db.query(Product).filter(Product.id == product_id).first()

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        return product.to_dict()


    @staticmethod
    def update_product(product_id, data, current_user, db):
        product = db.query(Product).filter(Product.id == product_id).first()

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        product.name = data.name
        product.sku = data.sku
        product.price = data.price
        product.quantity = data.quantity

        db.commit()
        db.refresh(product)

        AuditService.create_log(
            current_user["user_id"],
            "UPDATE",
            "PRODUCT",
            product.id,
            db
        )

        return {
            "message": "Product updated successfully",
            "product": product.to_dict()
        }


    @staticmethod
    def delete_product(product_id, current_user, db):
        product = db.query(Product).filter(Product.id == product_id).first()

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        AuditService.create_log(
            current_user["user_id"],
            "DELETE",
            "PRODUCT",
            product.id,
            db
        )

        db.delete(product)
        db.commit()

        return {"message": "Product deleted successfully"}