from typing import Generic, Literal

from loguru import logger
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from .abstraction import IRepository, Entity


class BaseRepository(IRepository[Entity], Generic[Entity]):
    model: Entity

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: str) -> Entity:
        q = select(self.model).where(self.model.id == id)
        result = await self.session.scalar(q)
        return result

    async def update(self, entity: Entity, **kwargs) -> Entity:
        q = update(self.model).where(self.model.id == entity.id).values(**kwargs)
        await self.session.execute(q)
        await self.session.commit()
        result = await self.get(entity.id)
        return result

    async def create(self, entity: Entity) -> Entity:
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    async def delete(self, id: str) -> Literal[True]:
        q = delete(self.model).where(self.model.id == id)
        await self.session.execute(q)
        await self.session.commit()
        return True

    async def all(self) -> list[Entity]:
        q = select(self.model)
        result = await self.session.scalars(q)
        if result:
            return result.fetchall()
