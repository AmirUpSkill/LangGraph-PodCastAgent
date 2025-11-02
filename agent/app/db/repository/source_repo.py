from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError

from app.db.models.source import Source, SourceStatus, SourceType
from app.db.repository.base_repo import BaseRepository

class SourceRepository(BaseRepository[Source]):
    """
        Repository for Source model
    """
    
    def __init__(self):
        super().__init__(Source)

    async def get_by_podcast_id(
        self, 
        db: AsyncSession, 
        podcast_id: str
    ) -> List[Source]:
        """
            Fetch all sources for a given podcast.
        """
        try:
            stmt = select(Source).where(Source.podcast_id == podcast_id)
            result = await db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError:
            await db.rollback()
            raise

    async def get_processed_sources_by_podcast(
        self, 
        db: AsyncSession, 
        podcast_id: str
    ) -> List[Source]:
        """
            Fetch only successfully processed sources for a podcast.
        """
        try:
            stmt = select(Source).where(
                Source.podcast_id == podcast_id,
                Source.status == SourceStatus.PROCESSED
            )
            result = await db.execute(stmt)
            return list(result.scalars().all())
        except SQLAlchemyError:
            await db.rollback()
            raise

    async def count_by_podcast_and_status(
        self, 
        db: AsyncSession, 
        podcast_id: str, 
        status: SourceStatus
    ) -> int:
        """
            Efficiently count sources by status without loading records into memory.
        """
        try:
            stmt = select(func.count()).select_from(Source).where(
                Source.podcast_id == podcast_id,
                Source.status == status
            )
            result = await db.execute(stmt)
            return result.scalar() or 0
        except SQLAlchemyError:
            await db.rollback()
            raise

    async def has_failed_sources(
        self, 
        db: AsyncSession, 
        podcast_id: str
    ) -> bool:
        """
            Check if any source failed processing (helper for service layer).
        """
        count = await self.count_by_podcast_and_status(
            db, podcast_id, SourceStatus.FAILED
        )
        return count > 0

    async def all_sources_processed(
        self, 
        db: AsyncSession, 
        podcast_id: str
    ) -> bool:
        """
            Check if all sources for a podcast have been processed.
        """
        try:
            total_stmt = select(func.count()).select_from(Source).where(
                Source.podcast_id == podcast_id
            )
            total_result = await db.execute(total_stmt)
            total = total_result.scalar() or 0

            if total == 0:
                return False

            processed = await self.count_by_podcast_and_status(
                db, podcast_id, SourceStatus.PROCESSED
            )
            
            return processed == total
        except SQLAlchemyError:
            await db.rollback()
            raise