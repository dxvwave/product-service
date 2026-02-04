import grpc
from infrastructure.clients.gen import auth_pb2, auth_pb2_grpc


class AuthClient:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.channel = None
        self.stub = None

    async def connect(self):
        if self.channel is None:
            self.channel = grpc.aio.insecure_channel(f"{self.host}:{self.port}")
            self.stub = auth_pb2_grpc.AuthServiceStub(self.channel)
            
    async def close(self):
        if self.channel:
            await self.channel.close()

    async def validate_token(self, token: str) -> bool:
        try:
            request = auth_pb2.ValidateRequest(token=token)
            response = await self.stub.ValidateToken(request)
            return response.is_valid
        except grpc.RpcError as e:
            print(f"gRPC error: {e.code()} - {e.details()}")
            return False
        
    async def close(self):
        await self.channel.close()


auth_client_instance = AuthClient(host="localhost", port=50051)
