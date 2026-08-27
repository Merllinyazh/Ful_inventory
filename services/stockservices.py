from fastapi import HTTPException
from pydantic import BaseModel
from models.database import Stock, Product, Location


class StockCreate(BaseModel):
    product_id: int
    location_id: int
    quantity: int


class StockService:

    @staticmethod
    def add_stock(data, db):

        if data.quantity < 0:
            raise HTTPException(status_code=400, detail="Quantity cannot be negative")

        product = db.query(Product).filter(Product.id == data.product_id).first()

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        location = db.query(Location).filter(Location.id == data.location_id).first()

        if not location:
            raise HTTPException(status_code=404, detail="Location not found")

        stock = db.query(Stock).filter(
            Stock.product_id == data.product_id,
            Stock.location_id == data.location_id
        ).first()

        if stock:
            stock.quantity += data.quantity
        else:
            stock = Stock(
                product_id=data.product_id,
                location_id=data.location_id,
                quantity=data.quantity
            )
            db.add(stock)

        db.commit()
        db.refresh(stock)

        return {
            "message": "Stock added successfully",
            "stock": stock.to_dict()
        }

    @staticmethod
    def get_stocks(db):
        stocks = db.query(Stock).all()
        return [stock.to_dict() for stock in stocks]

    @staticmethod
    def get_stock(product_id, location_id, db):

        stock = db.query(Stock).filter(
            Stock.product_id == product_id,
            Stock.location_id == location_id
        ).first()

        if not stock:
            raise HTTPException(status_code=404, detail="Stock not found")

        return stock.to_dict()