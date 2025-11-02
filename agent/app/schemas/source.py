from pydantic import BaseModel , Field 
from typing import Optional 
from datetime import datetime 
from app.db.models.source import SourceType , SourceStatus

# --- Here We define the Base Schema --- 
class SourceBase(BaseModel):
    type: SourceType
    raw_input: str = Field(..., description="The Original Input ")
# --- Create Schema : Used When Create New Source  --- 
class SourceCreate(SourceBase):
    pass 
# --- Response Schema --- 
class Source(SourceBase):
    id: str 
    podcast_id: str 
    status: SourceStatus = SourceStatus.PENDING
    content: Optional[str] = None 
    error_message: Optional[str] = None 
    created_at: datetime 
    class Config:
        from_attributes = True 