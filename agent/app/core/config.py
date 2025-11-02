from pydantic_settings import BaseSettings 
from pydantic import SecretStr, Field, computed_field
from typing import Optional 

class Settings(BaseSettings):
    # --- APP ---
    app_name: str = "PodCastAgent"
    debug: bool = False 
    # --- AI --- 
    gemini_api_key: SecretStr 
    firecrawl_api_key: SecretStr 
    # --- Supabase --- 
    supabase_url: str 
    supabase_anon_key: SecretStr 
    supabase_service_role_key: SecretStr 
    supabase_db_password: SecretStr  
    # --- Storage --- 
    supabase_audio_bucket: str 
    # --- Task Queue --- 
    redis_url: str 

    @computed_field
    @property
    def database_url(self) -> str:
        """Construct async PostgreSQL connection string for Supabase Transaction Pooler."""
        project_ref = self.supabase_url.split("//")[1].split(".")[0]
        password = self.supabase_db_password.get_secret_value()
        return f"postgresql+asyncpg://postgres.{project_ref}:{password}@aws-1-eu-west-3.pooler.supabase.com:6543/postgres"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

# --- Singleton Instance --- 
settings = Settings()
