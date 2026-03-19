from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Banco de dados
    db_user: str
    db_password: str
    db_name: str
    db_host: str
    db_port: int = 5432

    # LLM
    llm_api_key: str
    llm_model: str
    llm_base_url: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()  # type: ignore[call-arg]
