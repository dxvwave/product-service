from infrastructure.clients.auth_client import AuthClient, auth_client_instance


def get_auth_client() -> AuthClient:
    return auth_client_instance
