from fastapi import HTTPException
from pydantic import BaseModel
from models.database import Movement, Product, Location


class MovementCreate(BaseModel):
    product_id: int
    movement_type: str
    quantity: int
    from_location_id: int | None = None
    to_location_id: int | None = None


class MovementService:

    @staticmethod
    def create_movement(data, current_user, db):

        if data.quantity <= 0:
            raise HTTPException(status_code=400, detail="Quantity must be greater than zero")

        product = db.query(Product).filter(Product.id == data.product_id).first()

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        if data.movement_type not in ["IN", "OUT", "TRANSFER"]:
            raise HTTPException(status_code=400, detail="Invalid movement type")

        if data.movement_type == "IN":

            if not data.to_location_id:
                raise HTTPException(status_code=400, detail="Destination location is required")

            location = db.query(Location).filter(Location.id == data.to_location_id).first()

            if not location:
                raise HTTPException(status_code=404, detail="Location not found")

            product.quantity += data.quantity

        elif data.movement_type == "OUT":

            if not data.from_location_id:
                raise HTTPException(status_code=400, detail="Source location is required")

            if product.quantity < data.quantity:
                raise HTTPException(status_code=400, detail="Insufficient stock")

            product.quantity -= data.quantity

        elif data.movement_type == "TRANSFER":

            if not data.from_location_id or not data.to_location_id:
                raise HTTPException(status_code=400, detail="Both locations are required")

        movement = Movement(
            product_id=data.product_id,
            movement_type=data.movement_type,
            quantity=data.quantity,
            from_location_id=data.from_location_id,
            to_location_id=data.to_location_id,
            user_id=current_user["user_id"]
        )

        db.add(movement)
        db.commit()
        db.refresh(movement)

        return {"message": "Movement recorded successfully", "movement": movement.to_dict()}


    @staticmethod
    def get_movements(db):

        movements = db.query(Movement).all()

        return [movement.to_dict() for movement in movements]