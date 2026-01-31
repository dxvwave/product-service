from pydantic_settings import BaseSettings


class Config(BaseSettings):
    app_name: str = "Product Service"
    debug: bool = False
    database_url: str

    class Config:
        env_file = ".env"


settings = Config()
