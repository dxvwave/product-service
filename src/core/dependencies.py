from shared.dependencies import make_auth_dependencies

from services.product_service import ProductService, product_service
from interfaces.grpc.auth_client import AuthClient, auth_client_instance


def get_product_service() -> ProductService:
    return product_service


def get_auth_client() -> AuthClient:
    return auth_client_instance


get_current_user, get_current_active_user = make_auth_dependencies(get_auth_client)
