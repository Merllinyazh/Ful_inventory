from fastapi import FastAPI,Request
from config import engine, Base
import time
from utils.logger import logger
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

@app.middleware("http")
async def log_requests(request: Request, call_next):

    start_time = time.perf_counter()

    response = await call_next(request)

    process_time = (time.perf_counter() - start_time) * 1000

    logger.info(
        f"Method={request.method} "
        f"URL={request.url.path} "
        f"Status={response.status_code} "
        f"Duration={process_time:.2f}ms"
    )

    return response