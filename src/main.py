from fastapi import FastAPI
import uvicorn

from api.routes import router as v1_products_router

app = FastAPI(
    root_path="/api/v1/products",
)
app.include_router(v1_products_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
