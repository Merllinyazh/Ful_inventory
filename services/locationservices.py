from fastapi import HTTPException
from pydantic import BaseModel
from models.database import Location
from services.auditservices import AuditService


class LocationCreate(BaseModel):
    name: str
    address: str | None = None


class LocationService:

    @staticmethod
    def create_location(data, current_user, db):
        location = db.query(Location).filter(
            Location.name == data.name
        ).first()

        if location:
            raise HTTPException(
                status_code=409,
                detail="Location already exists"
            )

        location = Location(
            name=data.name,
            address=data.address
        )

        db.add(location)
        db.commit()
        db.refresh(location)

        # Audit log
        AuditService.create_log(
            user_id=current_user["user_id"],
            action="CREATE_LOCATION",
            details=f"Location '{location.name}' created",
            db=db
        )

        return {
            "message": "Location created successfully",
            "location": location.to_dict()
        }

    @staticmethod
    def get_locations(db):
        locations = db.query(Location).all()
        return [location.to_dict() for location in locations]

    @staticmethod
    def get_location(location_id, db):
        location = db.query(Location).filter(
            Location.id == location_id
        ).first()

        if not location:
            raise HTTPException(
                status_code=404,
                detail="Location not found"
            )

        return location.to_dict()

    @staticmethod
    def update_location(location_id, data, current_user, db):
        location = db.query(Location).filter(
            Location.id == location_id
        ).first()

        if not location:
            raise HTTPException(
                status_code=404,
                detail="Location not found"
            )

        location.name = data.name
        location.address = data.address

        db.commit()
        db.refresh(location)

        # Audit log
        AuditService.create_log(
            user_id=current_user["user_id"],
            action="UPDATE_LOCATION",
            details=f"Location '{location.name}' updated",
            db=db
        )

        return {
            "message": "Location updated successfully",
            "location": location.to_dict()
        }

    @staticmethod
    def delete_location(location_id, current_user, db):
        location = db.query(Location).filter(
            Location.id == location_id
        ).first()

        if not location:
            raise HTTPException(
                status_code=404,
                detail="Location not found"
            )

        location_name = location.name

        # Audit before deleting
        AuditService.create_log(
            user_id=current_user["user_id"],
            action="DELETE_LOCATION",
            details=f"Location '{location_name}' deleted",
            db=db
        )

        db.delete(location)
        db.commit()

        return {
            "message": "Location deleted successfully"
        }