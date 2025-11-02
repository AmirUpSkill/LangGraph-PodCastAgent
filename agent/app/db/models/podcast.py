from typing import Optional, List
import enum
from sqlalchemy import String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from .base import Base

# --- Status Model ---
class PodcastStatus(str, enum.Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"
# --- The Podcast Model ---
class Podcast(Base):
    __tablename__ = "podcasts"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    status: Mapped[PodcastStatus] = mapped_column(Enum(PodcastStatus), default=PodcastStatus.PENDING)
    script: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    audio_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    sources: Mapped[List["Source"]] = relationship(back_populates="podcast", cascade="all, delete-orphan")