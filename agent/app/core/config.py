from pydantic_settings import BaseSettings 
from pydantic import SecretStr , Field 
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
    # --- Storage --- 
    supabase_audio_bucket: str 
    # --- Task Queue --- 
    redis_url: str 

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"
# --- Singleton Instance --- 
settings = Settings()
