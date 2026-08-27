from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime,Float,ForeignKey
from config import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(50), default="staff")
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {"id": self.id, "username": self.username, "email": self.email, "role": self.role}

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    sku = Column(String(100), unique=True, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "sku": self.sku,
            "price": self.price,
            "quantity": self.quantity
        }

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    address = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "address": self.address}

class Movement(Base):
    __tablename__ = "movements"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    movement_type = Column(String(20), nullable=False)
    quantity = Column(Integer, nullable=False)
    from_location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    to_location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "movement_type": self.movement_type,
            "quantity": self.quantity,
            "from_location_id": self.from_location_id,
            "to_location_id": self.to_location_id,
            "user_id": self.user_id,
            "created_at": self.created_at
        }