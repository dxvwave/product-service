"""Custom exceptions for the product service."""


class ProductServiceException(Exception):
    """Base exception for product service."""

    pass


class ProductNotFoundError(ProductServiceException):
    """Raised when a product is not found."""

    pass


class ProductAlreadyExistsError(ProductServiceException):
    """Raised when trying to create a product that already exists."""

    pass


class InvalidProductDataError(ProductServiceException):
    """Raised when product data is invalid."""

    pass
