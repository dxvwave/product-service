from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
import uvicorn

from api.routes import router as v1_products_router
from infrastructure.clients.auth_client import auth_client_instance


@asynccontextmanager
async def lifespan(app: FastAPI):
    await auth_client_instance.connect()
    app.state.auth_client = auth_client_instance
    
    yield
    
    await auth_client_instance.close()

app = FastAPI(
    root_path="/api/v1/products",
    lifespan=lifespan,
)
app.include_router(v1_products_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
