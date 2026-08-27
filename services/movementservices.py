from fastapi import HTTPException
from pydantic import BaseModel
from models.database import Product, Location, Stock, Movement
from services.auditservices import AuditService


class MovementCreate(BaseModel):
    product_id: int
    from_location_id: int | None = None
    to_location_id: int | None = None
    quantity: int
    movement_type: str


class MovementService:

    @staticmethod
    def create_movement(data, current_user, db):

        product = db.query(Product).filter(
            Product.id == data.product_id
        ).first()

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        if data.quantity <= 0:
            raise HTTPException(
                status_code=400,
                detail="Quantity must be greater than 0"
            )

        movement_type = data.movement_type.upper()

        # STOCK IN
        if movement_type == "IN":

            if not data.to_location_id:
                raise HTTPException(
                    status_code=400,
                    detail="Destination location required"
                )

            location = db.query(Location).filter(
                Location.id == data.to_location_id
            ).first()

            if not location:
                raise HTTPException(
                    status_code=404,
                    detail="Location not found"
                )

            stock = db.query(Stock).filter(
                Stock.product_id == data.product_id,
                Stock.location_id == data.to_location_id
            ).first()

            if not stock:
                stock = Stock(
                    product_id=data.product_id,
                    location_id=data.to_location_id,
                    quantity=0
                )
                db.add(stock)

            stock.quantity += data.quantity


        # STOCK OUT
        elif movement_type == "OUT":

            if not data.from_location_id:
                raise HTTPException(
                    status_code=400,
                    detail="Source location required"
                )

            stock = db.query(Stock).filter(
                Stock.product_id == data.product_id,
                Stock.location_id == data.from_location_id
            ).first()

            if not stock or stock.quantity < data.quantity:
                raise HTTPException(
                    status_code=400,
                    detail="Insufficient stock"
                )

            stock.quantity -= data.quantity


        # TRANSFER
        elif movement_type == "TRANSFER":

            if not data.from_location_id or not data.to_location_id:
                raise HTTPException(
                    status_code=400,
                    detail="Source and destination locations required"
                )

            source_stock = db.query(Stock).filter(
                Stock.product_id == data.product_id,
                Stock.location_id == data.from_location_id
            ).first()

            if not source_stock or source_stock.quantity < data.quantity:
                raise HTTPException(
                    status_code=400,
                    detail="Insufficient stock"
                )

            destination_stock = db.query(Stock).filter(
                Stock.product_id == data.product_id,
                Stock.location_id == data.to_location_id
            ).first()

            if not destination_stock:
                destination_stock = Stock(
                    product_id=data.product_id,
                    location_id=data.to_location_id,
                    quantity=0
                )
                db.add(destination_stock)

            source_stock.quantity -= data.quantity
            destination_stock.quantity += data.quantity

        else:
            raise HTTPException(
                status_code=400,
                detail="Movement type must be IN, OUT or TRANSFER"
            )

        # Create movement record
        movement = Movement(
            product_id=data.product_id,
            from_location_id=data.from_location_id,
            to_location_id=data.to_location_id,
            quantity=data.quantity,
            movement_type=movement_type,
            user_id=current_user["user_id"]
        )

        db.add(movement)
        db.commit()
        db.refresh(movement)

        # Create audit log
        AuditService.create_log(
            user_id=current_user["user_id"],
            action=f"STOCK_{movement_type}",
            details=(
                f"{movement_type} movement: "
                f"Product '{product.name}', "
                f"Quantity {data.quantity}, "
                f"From location {data.from_location_id}, "
                f"To location {data.to_location_id}"
            ),
            db=db
        )

        return {
            "message": "Movement completed successfully",
            "movement": movement.to_dict()
        }