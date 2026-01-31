from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name: str = Field(..., example="Sample Product")
    description: str = Field(..., example="This is a sample product.")
    price: float = Field(..., example=19.99)
    quantity: int = Field(..., example=100)


class ProductRead(ProductBase):
    id: int = Field(..., example=1)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    name: str | None = Field(None, example="Sample Product")
    description: str | None = Field(None, example="This is a sample product.")
    price: float | None = Field(None, example=19.99)
    quantity: int | None = Field(None, example=100)
