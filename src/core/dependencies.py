from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from google.protobuf.json_format import MessageToDict

from services.product_service import product_service, ProductService
from interfaces.grpc.auth_client import AuthClient, auth_client_instance
from src.core.exceptions import UnauthorizedError


def get_product_service() -> ProductService:
    """Get the product service instance."""
    return product_service


def get_auth_client() -> AuthClient:
    """Get the auth client instance."""
    return auth_client_instance


async def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    auth_client: AuthClient = Depends(get_auth_client),
) -> dict:
    response = await auth_client.validate_token(token.credentials)
    
    if not response.is_valid:
        raise UnauthorizedError("Invalid authentication token")
    
    return MessageToDict(
        response.user, 
        preserving_proto_field_name=True,
        always_print_fields_with_no_presence=True,
    )


async def get_current_active_user(
    current_user: dict = Depends(get_current_user),
) -> dict:
    if not current_user.get("is_active", False):
        raise UnauthorizedError("Inactive user")
    return current_user
