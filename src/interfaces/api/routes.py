import logging

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import ProductRead, ProductCreate, ProductUpdate
from db import db_session_manager
from core.dependencies import (
    get_current_active_user,
    get_product_service,
)
from services.product_service import ProductService

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
    current_user: dict = Depends(get_current_active_user),
):
    new_product = await product_service.create_product(
        session,
        product,
        current_user.get("id"),
    )
    return new_product


@router.get("/{product_id}", response_model=ProductRead)
async def get_product(
    product_id: int,
    session: AsyncSession = Depends(db_session_manager.get_async_session),
    product_service: ProductService = Depends(get_product_service),
):
    product = await product_service.get_product_by_id(session, product_id)
    return product


@router.put("/{product_id}", response_model=ProductRead)
async def update_product(
    product_id: int,
    product_update: ProductUpdate,
    session: AsyncSession = Depends(db_session_manager.get_async_session),
    product_service: ProductService = Depends(get_product_service),
    current_user: dict = Depends(get_current_active_user),
):
    product = await product_service.update_product(
        session,
        product_id,
        product_update,
        current_user.get("id"),
    )
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    session: AsyncSession = Depends(db_session_manager.get_async_session),
    product_service: ProductService = Depends(get_product_service),
    current_user: dict = Depends(get_current_active_user),
):
    await product_service.delete_product(
        session,
        product_id,
        current_user.get("id"),
    )
