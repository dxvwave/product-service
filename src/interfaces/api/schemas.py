from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class ProductBase(BaseModel):
    """Base product schema with common fields."""

    name: str = Field(
        ...,
        example="Sample Product",
        min_length=1,
        max_length=255,
    )
    description: str = Field(
        ...,
        example="This is a sample product.",
        min_length=1,
    )
    price: float = Field(
        ...,
        example=19.99,
        gt=0,
    )
    quantity: int = Field(
        ...,
        example=100,
        ge=0,
    )


class ProductCreate(ProductBase):
    """Schema for creating a new product."""

    pass


class ProductUpdate(BaseModel):
    """Schema for updating an existing product."""

    name: str | None = Field(
        None,
        example="Sample Product",
        min_length=1,
        max_length=255,
    )
    description: str | None = Field(
        None,
        example="This is a sample product.",
        min_length=1,
    )
    price: float | None = Field(
        None,
        example=19.99,
        gt=0,
    )
    quantity: int | None = Field(
        None,
        example=100,
        ge=0,
    )


class ProductRead(ProductBase):
    """Schema for reading product data."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., example=1)
    user_id: int = Field(..., example=1)
    created_at: datetime
    updated_at: datetime
