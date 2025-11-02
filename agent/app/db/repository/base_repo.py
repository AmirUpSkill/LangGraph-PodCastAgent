from typing import TypeVar, Generic, Optional, List, Protocol
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.exc import SQLAlchemyError
import uuid

# --- Define a Protocol for models with an 'id' attribute ---
class HasID(Protocol):
    id: str

# --- Define the Model Type with constraint ---
ModelType = TypeVar("ModelType", bound=DeclarativeBase)

class BaseRepository(Generic[ModelType]):
    """
    Generic Base repository providing common CRUD operations
    """
    def __init__(self, model: type[ModelType]):
        self.model = model
    
    # --- get single Record ---
    async def get(self, db: AsyncSession, id: str) -> Optional[ModelType]:
        """
        Fetch A Single Record By Id
        """
        try:
            result = await db.execute(
                select(self.model).where(self.model.id == id)  # type: ignore
            )
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            print(f"Error fetching record with id {id}: {e}")
            return None
    
    # --- get multiple records ---
    async def get_multi(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
    ) -> List[ModelType]:
        """
        Fetch Multiple Records With Pagination
        """
        try:
            result = await db.execute(
                select(self.model).offset(skip).limit(limit)  # Fixed: was self._model
            )
            return list(result.scalars().all())
        except SQLAlchemyError:
            await db.rollback()
            raise
    
    # --- Create a new record ---
    async def create(self, db: AsyncSession, *, obj_in: ModelType) -> ModelType:
        """
        Create a new record in the database
        """
        try:
            # --- Generate UUID if not provided ---
            if not hasattr(obj_in, 'id') or not obj_in.id:  # type: ignore
                obj_in.id = str(uuid.uuid4())  # type: ignore
            db.add(obj_in)
            await db.commit()
            await db.refresh(obj_in)
            return obj_in
        except SQLAlchemyError:
            await db.rollback()
            raise
    
    # --- Update an existing record ---
    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        update_data: dict
    ) -> ModelType:
        """
        Update an existing record in the database
        """
        try:
            for field, value in update_data.items():
                setattr(db_obj, field, value)
            await db.commit()
            await db.refresh(db_obj)
            return db_obj
        except SQLAlchemyError:
            await db.rollback()
            raise
    
    # --- Delete a record ---
    async def delete(
        self,
        db: AsyncSession,
        *,
        id: str
    ) -> bool:
        """
        Delete a record by ID. Return True if deleted, False if not found.
        """
        try:
            obj = await self.get(db, id)
            if obj:
                await db.delete(obj)
                await db.commit()
                return True
            return False
        except SQLAlchemyError:
            await db.rollback()
            raise