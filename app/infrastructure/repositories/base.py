from typing import Generic, Literal

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

    async def get_by(self, is_many: bool = False, with_unique: bool = False, **kwargs) -> Entity | list[Entity]:
        where_by_clauses = []
        for key, value in kwargs.items():
            clause = getattr(self.model, key) == value
            where_by_clauses.append(clause)

        q = select(self.model).where(*where_by_clauses)
        if not is_many:
            result = await self.session.scalar(q)
        else:
            result = await self.session.scalars(q)

        if result:
            if is_many:
                if with_unique:
                    return result.unique().all()
                return result.all()
            else:
                return result
        else:
            if is_many:
                return []
            return

    async def update(self, id: str, **kwargs) -> Entity:
        q = update(self.model).where(self.model.id == id).values(**kwargs)
        await self.session.execute(q)
        await self.session.commit()
        result = await self.get(id)
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

    async def direct_delete(self, id: str) -> Literal[True]:
        instance = await self.get(id)
        await self.session.delete(instance)
        await self.session.commit()
        return True

    async def all(self, with_unique: bool = False) -> list[Entity]:
        q = select(self.model)
        result = await self.session.scalars(q)
        if result:
            if with_unique:
                return result.unique().all()
            return result.all()
        return []
