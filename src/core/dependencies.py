from services.product_service import product_service, ProductService
from interfaces.grpc.auth_client import AuthClient, auth_client_instance


def get_product_service() -> ProductService:
    """Get the product service instance."""
    return product_service


def get_auth_client() -> AuthClient:
    """Get the auth client instance."""
    return auth_client_instance
