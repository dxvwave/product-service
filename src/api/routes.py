from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from .schemas import ProductRead, ProductCreate, ProductUpdate
from core.db import db_session_manager
from core.models import Product
from core.dependencies import get_auth_client
from infrastructure.clients.auth_client import AuthClient

router = APIRouter(
    tags=["products"],
)


@router.get("/", response_model=list[ProductRead])
async def get_products(
    session: AsyncSession = Depends(db_session_manager.get_async_session),
):
    products = await session.scalars(select(Product))
    return products.all()


@router.post("/", response_model=ProductRead)
async def create_product(
    product: ProductCreate,
    session: AsyncSession = Depends(db_session_manager.get_async_session),
):
    new_product = Product(**product.model_dump())
    session.add(new_product)
    await session.commit()
    await session.refresh(new_product)
    return ProductRead(**new_product.__dict__)


@router.get("/{product_id}", response_model=ProductRead)
async def get_product(
    product_id: int,
    session: AsyncSession = Depends(db_session_manager.get_async_session),
):
    product = await session.scalar(select(Product).where(Product.id == product_id))
    if not product:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": f"Product: {product_id} not found"},
        )
    return ProductRead(product.__dict__)


@router.put("/{product_id}", response_model=ProductRead)
async def update_product(
    product_id: int,
    product_update: ProductUpdate,
    session: AsyncSession = Depends(db_session_manager.get_async_session),
):
    product = await session.scalar(select(Product).where(Product.id == product_id))
    if not product:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": f"Product: {product_id} not found"},
        )

    for key, value in product_update.model_dump(exclude_unset=True).items():
        setattr(product, key, value)

    session.add(product)
    await session.commit()
    await session.refresh(product)
    return ProductRead(**product.__dict__)


@router.delete("/{product_id}")
async def delete_product(
    product_id: int,
    session: AsyncSession = Depends(db_session_manager.get_async_session),
):
    product = await session.scalar(select(Product).where(Product.id == product_id))
    if not product:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": f"Product: {product_id} not found"},
        )
    await session.delete(product)
    await session.commit()


@router.get("/secure-data/")
async def get_secure_data(
    token: str,
    auth_client: AuthClient = Depends(get_auth_client),
):
    is_valid = await auth_client.validate_token(token)

    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Invalid authentication token"},
        )

    return {
        "secure_data": "This is some secure data accessible only with a valid token."
    }
