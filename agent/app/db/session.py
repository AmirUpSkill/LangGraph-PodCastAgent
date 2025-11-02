from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator
from app.core.config import settings

# --- Create Async Engine ---
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,  # --- This Will Log SQL queries if debug mode is on ---
    pool_pre_ping=True,   # ---- This Will Verify connections before using them ---
    pool_size=5,          # --- Connection pool size ---
    max_overflow=10,      # --- Max overflow connections ---
    # --- Disable prepared statements for Supabase transaction pooler compatibility ----
    connect_args={
        "prepared_statement_cache_size": 0,
        "statement_cache_size": 0,
        "server_settings": {
            "jit": "off",  
        }
    },
    execution_options={
        "compiled_cache": None  
    }
)

# --- Create Async Session Factory ---
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  
    autocommit=False,
    autoflush=False
)

# --- Dependency for FastAPI ---
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Provides a database session for dependency injection in FastAPI routes.
    Automatically handles session cleanup.
    
    Usage in FastAPI:
        @app.get("/podcasts/{podcast_id}")
        async def get_podcast(podcast_id: str, db: AsyncSession = Depends(get_db)):
            ...
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()