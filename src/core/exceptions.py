from fastapi import status

from shared.exceptions import ApplicationException, AuthenticationError, UnauthorizedError, InactiveUserError  # noqa: F401


class ProductServiceException(ApplicationException):
    pass


class ProductNotFoundError(ProductServiceException):
    pass


class ProductAlreadyExistsError(ProductServiceException):
    pass


class InvalidProductDataError(ProductServiceException):
    pass


EXCEPTION_MAPPING = {
    ProductNotFoundError: status.HTTP_404_NOT_FOUND,
    ProductAlreadyExistsError: status.HTTP_409_CONFLICT,
    InvalidProductDataError: status.HTTP_400_BAD_REQUEST,
    UnauthorizedError: status.HTTP_401_UNAUTHORIZED,
    InactiveUserError: status.HTTP_403_FORBIDDEN,
}
