from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "G.A.R.D."
    database_url: str = "sqlite:///./gard.db"
    cors_origins: list[str] = ["http://localhost:4200"]

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
