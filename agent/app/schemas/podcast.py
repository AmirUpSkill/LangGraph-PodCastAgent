from pydantic import BaseModel , Field 
from typing import Optional , List 
from datetime import datetime

from pydantic.mypy import from_attributes_callback
from .source import Source 
from app.db.models.podcast import PodcastStatus

# --- Base Schema --- 
class PodcastBase(BaseModel):
    title: str = Field(..., min_length=3 , max_length=255, description="The tile of Podcast")
# --- Create Schema --- 
class PodcastCreate(PodcastBase):
    pass
# --- Response Schema --- 
class Podcast(PodcastBase):
    id: str 
    status: PodcastStatus = PodcastStatus.PENDING
    script: Optional[str] = None 
    audio_url: Optional[str] = None 
    error_message: Optional[str] = None 
    created_at: datetime 
    updated_at: datetime 
    sources: List[Source] = []
    class Config:
        from_attributes = True 