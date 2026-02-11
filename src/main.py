import logging

import uvicorn
from fastapi import FastAPI, status
from fastapi.concurrency import asynccontextmanager
from fastapi.responses import JSONResponse

from core.logging_config import setup_logging
from core.exceptions import EXCEPTION_MAPPING, ApplicationException
from interfaces.api.routes import router as products_router
from interfaces.grpc.auth_client import auth_client_instance

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for the FastAPI application."""
    # Startup
    logger.info("Starting product service...")
    await auth_client_instance.connect()
    app.state.auth_client = auth_client_instance
    logger.info("Auth client connected")

    yield

    # Shutdown
    logger.info("Shutting down product service...")
    await auth_client_instance.close()
    logger.info("Auth client closed")


app = FastAPI(
    title="Product Service",
    description="Product Management Service for Microservices",
    version="0.1.2",
    root_path="/api/v1/products",
    lifespan=lifespan,
)


# Global exception handler for application exceptions
@app.exception_handler(ApplicationException)
async def application_exception_handler(request, exc: ApplicationException):
    status_code = EXCEPTION_MAPPING.get(
        type(exc),
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    )

    return JSONResponse(
        status_code=status_code,
        content={"message": exc.message},
    )


# Include routers with tags
app.include_router(products_router)


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "product-service",
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
