import logging

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from google.protobuf.json_format import MessageToDict

from .schemas import ProductRead, ProductCreate, ProductUpdate
from db import db_session_manager
from core.dependencies import get_product_service, get_auth_client
from core.exceptions import ProductNotFoundError
from services.product_service import ProductService
from interfaces.grpc.auth_client import AuthClient

logger = logging.getLogger(__name__)

router = APIRouter(
    tags=["Products"],
)


@router.get("/", response_model=list[ProductRead])
async def get_products(
    session: AsyncSession = Depends(db_session_manager.get_async_session),
    product_service: ProductService = Depends(get_product_service),
):
    products = await product_service.get_all_products(session)
    return products


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: ProductCreate,
    session: AsyncSession = Depends(db_session_manager.get_async_session),
    product_service: ProductService = Depends(get_product_service),
):
    new_product = await product_service.create_product(session, product)
    return new_product


@router.get("/{product_id}", response_model=ProductRead)
async def get_product(
    product_id: int,
    session: AsyncSession = Depends(db_session_manager.get_async_session),
    product_service: ProductService = Depends(get_product_service),
):
    try:
        product = await product_service.get_product_by_id(session, product_id)
        return product
    except ProductNotFoundError as e:
        logger.warning(f"Product not found: {product_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.put("/{product_id}", response_model=ProductRead)
async def update_product(
    product_id: int,
    product_update: ProductUpdate,
    session: AsyncSession = Depends(db_session_manager.get_async_session),
    product_service: ProductService = Depends(get_product_service),
):
    try:
        product = await product_service.update_product(session, product_id, product_update)
        return product
    except ProductNotFoundError as e:
        logger.warning(f"Product not found for update: {product_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    session: AsyncSession = Depends(db_session_manager.get_async_session),
    product_service: ProductService = Depends(get_product_service),
):
    try:
        await product_service.delete_product(session, product_id)
    except ProductNotFoundError as e:
        logger.warning(f"Product not found for deletion: {product_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.get("/user-data/")
async def get_user_data(
    token: str = Depends(HTTPBearer()),
    auth_client: AuthClient = Depends(get_auth_client),
):
    response = await auth_client.validate_token(token.credentials)

    if not response.is_valid:
        logger.warning("Invalid authentication token provided")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        )

    user_data = MessageToDict(
        response.user,
        always_print_fields_with_no_presence=True,
        preserving_proto_field_name=True,
    )

    return user_data
