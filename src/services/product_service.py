import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Product
from interfaces.api.schemas import ProductCreate, ProductUpdate
from core.exceptions import ProductNotFoundError
from services.rabbitmq_client import rabbit_client

logger = logging.getLogger(__name__)


class ProductService:
    """Service for product management operations."""

    async def get_product_by_id(
        self,
        session: AsyncSession,
        product_id: int,
    ) -> Product:
        """
        Get a product by its ID.

        Args:
            session: Database session
            product_id: Product ID

        Returns:
            Product object

        Raises:
            ProductNotFoundError: If product is not found
        """
        product = await session.get(Product, product_id)

        if not product:
            logger.debug(f"Product not found with id: {product_id}")
            raise ProductNotFoundError(f"Product with id {product_id} not found")

        return product

    async def get_all_products(
        self,
        session: AsyncSession,
    ) -> list[Product]:
        """
        Get all products.

        Args:
            session: Database session

        Returns:
            List of all products
        """
        result = await session.scalars(select(Product))
        return list(result.all())

    async def create_product(
        self,
        session: AsyncSession,
        product_data: ProductCreate,
        user_id: int,
    ) -> Product:
        """
        Create a new product.

        Args:
            session: Database session
            product_data: Product creation data
            user_id: int: ID of the user creating the product

        Returns:
            Created product object
        """
        new_product = Product(**product_data.model_dump(), user_id=user_id)

        session.add(new_product)
        await session.commit()
        await session.refresh(new_product)

        logger.info(f"Created new product: {new_product.name} (ID: {new_product.id})")

        await rabbit_client.publish_product_created(
            {
                "id": new_product.id,
                "name": new_product.name,
                "description": new_product.description,
                "price": str(new_product.price),
                "user_id": new_product.user_id,
            }
        )

        logger.info(f"Published product.created event for product ID: {new_product.id}")

        return new_product

    async def update_product(
        self,
        session: AsyncSession,
        product_id: int,
        product_data: ProductUpdate,
        user_id: int,
    ) -> Product:
        """
        Update an existing product.

        Args:
            session: Database session
            product_id: Product ID
            product_data: Product update data
            user_id: int: ID of the user attempting to update the product

        Returns:
            Updated product object

        Raises:
            ProductNotFoundError: If product is not found
        """
        product = await self.get_product_by_id(session, product_id)
        previous_price = product.price

        if product.user_id != user_id:
            logger.debug(
                f"User {user_id} is not authorized to update product {product_id}"
            )
            raise ProductNotFoundError(f"Product with id {product_id} not found")
        
        update_data = product_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(product, key, value)

        session.add(product)
        await session.commit()
        await session.refresh(product)

        logger.info(f"Updated product: {product.name} (ID: {product.id})")

        if "price" in update_data and update_data["price"] != previous_price:
            await rabbit_client.publish_product_price_changed(
                {
                    "id": product.id,
                    "user_id": product.user_id,
                    "previous_price": str(previous_price),
                    "new_price": str(product.price),
                }
            )

        return product

    async def delete_product(
        self,
        session: AsyncSession,
        product_id: int,
        user_id: int,
    ) -> None:
        """
        Delete a product.

        Args:
            session: Database session
            product_id: Product ID
            user_id: int: ID of the user attempting to delete the product

        Raises:
            ProductNotFoundError: If product is not found
        """
        product = await self.get_product_by_id(session, product_id)

        if product.user_id != user_id:
            logger.debug(
                f"User {user_id} is not authorized to delete product {product_id}"
            )
            raise ProductNotFoundError(f"Product with id {product_id} not found")

        await session.delete(product)
        await session.commit()

        logger.info(f"Deleted product: {product.name} (ID: {product.id})")


product_service = ProductService()
