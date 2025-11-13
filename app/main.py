from fastapi import FastAPI
from app.api import router
from app.database import create_tables

app = FastAPI(
    title="WB Sales API",
    description="API для работы с данными продаж Wildberries",
    version="1.0.0"
)

app.include_router(router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    await create_tables()
    print("Database tables created!")

@app.get("/")
async def root():
    return {
        "message": "WB Sales API is running!",
        "endpoints": {
            "get_category": "/api/v1/category/{id}",
            "get_sellers": "/api/v1/sellers/",
            "get_seller": "/api/v1/sellers/{id}",
            "get_products": "/api/v1/products/",
            "update_data": "/api/v1/update/{id}"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)