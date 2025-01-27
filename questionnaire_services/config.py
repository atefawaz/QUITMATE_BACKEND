from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # JWT configuration
    secret_key: str = "your_secret_key"  # Replace with the actual secret key
    algorithm: str = "HS256"  # JWT algorithm
    access_token_expire_minutes: int = 30  # Token expiry in minutes

    # Database configuration
    database_url: str  # Database URL for connecting to your PostgreSQL database

    # Load from .env file
    class Config:
        env_file = ".env"  # Specify the .env file for environment variables


# Initialize the settings instance
settings = Settings()
