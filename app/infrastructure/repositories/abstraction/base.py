from abc import ABC
from typing import TypeVar, Generic

from infrastructure.entities.base import BaseModel

Entity = TypeVar("Entity", bound=BaseModel)


class IRepository(ABC, Generic[Entity]):
    async def get(self, id: str):
        raise NotImplementedError

    async def create(self, entity: Entity):
        raise NotImplementedError

    async def update(self, entity: Entity):
        raise NotImplementedError

    async def delete(self, id: str):
        raise NotImplementedError
