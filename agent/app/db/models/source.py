from typing import Optional 
import enum
from sqlalchemy import String , Text , Enum , ForeignKey, DateTime
from sqlalchemy.orm import Mapped , mapped_column , relationship 
from datetime import datetime, timezone
from .base import Base

# --- Type Of Sources --- 
class SourceType(str, enum.Enum):
    URL = "URL"
    NOTES = "NOTES"
    PDF = "PDF"
# --- Status Of the Processing ---
class SourceStatus(str, enum.Enum):
    PENDING = "PENDING"
    PROCESSED = "PROCESSED"
    FAILED = "FAILED"

class Source(Base):
    __tablename__ = "sources"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    podcast_id: Mapped[str] = mapped_column(ForeignKey("podcasts.id", ondelete="CASCADE"))
    type: Mapped[SourceType] = mapped_column(Enum(SourceType))
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  
    raw_input: Mapped[str] = mapped_column(Text)  
    status: Mapped[SourceStatus] = mapped_column(Enum(SourceStatus), default=SourceStatus.PENDING)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    podcast: Mapped["Podcast"] = relationship(back_populates="sources")


