from typing import Optional, List, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError

from app.db.models.podcast import Podcast, PodcastStatus
from app.db.repository.base_repo import BaseRepository

class PodcastRepository(BaseRepository[Podcast]):
    """
        Repository for Podcast model
    """
    def __init__(self):
        super().__init__(Podcast)
    async def get_with_sources(
        self,
        db: AsyncSession,
        podcast_id: str 
    ) -> Optional[Podcast]:
        """
            Fetch Podcast with all related sources in a single query . 
            Essential for AI Context aggregation 
        """
        try:
            stmt = (
                select(Podcast)
                .where(Podcast.id == podcast_id)
                .options(selectinload(Podcast.sources))    
            )
            result = await db.execute(stmt)
            return result.scalar_one_or_none()
        except SQLAlchemyError:
            await db.rollback()
            raise
    # --- Get the Status Of the Podcast Generation --- 
    async def get_by_status(
        self,
        db: AsyncSession,
        status: PodcastStatus
    ) -> List[Podcast]:
        """
            Fetch all podcasts with a specific status 
        """ 
        try:
            stmt = select(Podcast).where(Podcast.status == status)
            result = await db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError:
            await db.rollback()
            raise 
    # --- Update Status of the Job --- 
    async def update_status(
        self,
        db: AsyncSession,
        podcast_id: str,
        status: PodcastStatus,
        *,
        script: Optional[str] = None,
        audio_url: Optional[str] = None,
        error_message: Optional[str] = None,
    ) -> Optional[Podcast]:
        """
            Atomically update podcast status along with optional fields.
            Ensures state consistency for the workflow state machine.
        """
        try:
            podcast = await self.get(db, podcast_id)
            if not podcast:
                return None
            
            update_data: dict[str, Any] = {"status": status}
            
            if script is not None:
                update_data["script"] = script
            if audio_url is not None:
                update_data["audio_url"] = audio_url
            if error_message is not None:
                update_data["error_message"] = error_message
            
            return await self.update(db, db_obj=podcast, update_data=update_data)
        except SQLAlchemyError:
            await db.rollback()
            raise