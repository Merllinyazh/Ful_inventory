from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config import SessionLocal
from routes.auth import get_current_user, admin_required
from services.locationservices import LocationService, LocationCreate

router = APIRouter(prefix="/locations", tags=["Locations"])


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("/", status_code=201)
def create_location(
    data: LocationCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(admin_required)
):
    return LocationService.create_location(
        data,
        current_user,
        db
    )


@router.get("/")
def get_locations(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return LocationService.get_locations(db)


@router.get("/{location_id}")
def get_location(
    location_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return LocationService.get_location(location_id, db)


@router.put("/{location_id}")
def update_location(
    location_id: int,
    data: LocationCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(admin_required)
):
    return LocationService.update_location(location_id, data, db)


@router.delete("/{location_id}")
def delete_location(
    location_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(admin_required)
):
    return LocationService.delete_location(location_id, db)