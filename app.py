from fastapi import FastAPI
from config import engine, Base
from models.database import User
from routes.auth import router as auth_router
from routes.product import router as product_router
from routes.location import router as location_router
from routes.movement import router as movement_router
from routes.stocks import router as stock_router

app = FastAPI(title="Inventory Management API", version="1.0.0")

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(product_router)
app.include_router(location_router)
app.include_router(movement_router)
app.include_router(stock_router)

@app.get("/")
def home():
    return {"message": "Inventory Management API is running"}