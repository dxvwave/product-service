import grpc
from grpc_apps.gen import auth_pb2, auth_pb2_grpc


class AuthClient:
    def __init__(self, host="localhost", port=50051):
        self.channel = grpc.insecure_channel(f"{host}:{port}")
        self.stub = auth_pb2_grpc.AuthServiceStub(self.channel)

    def validate_token(self, token: str) -> bool:
        try:
            request = auth_pb2.ValidateRequest(token=token)
            response = self.stub.ValidateToken(request)
            return response.is_valid
        except grpc.RpcError as e:
            print(f"gRPC error: {e.code()} - {e.details()}")
            return False
