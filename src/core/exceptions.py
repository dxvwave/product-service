"""Custom exceptions for the application."""

from fastapi import status


class ApplicationException(Exception):
    """Base exception for the application."""

    def __init__(self, message: str):
        self.message = message


class ProductServiceException(ApplicationException):
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


class AuthenticationError(ApplicationException):
    """Raised when authentication fails."""

    pass


class UnauthorizedError(AuthenticationError):
    """Raised when a user is not authorized to perform an action."""

    pass


class InactiveUserError(AuthenticationError):
    """Raised when an inactive user attempts to perform an action."""

    pass


EXCEPTION_MAPPING = {
    ProductNotFoundError: status.HTTP_404_NOT_FOUND,
    ProductAlreadyExistsError: status.HTTP_409_CONFLICT,
    InvalidProductDataError: status.HTTP_400_BAD_REQUEST,
    UnauthorizedError: status.HTTP_401_UNAUTHORIZED,
    InactiveUserError: status.HTTP_403_FORBIDDEN,
}
