from .base import BaseRepository
from ..entities import GroupModel


class GroupRepository(BaseRepository[GroupModel]):
    model = GroupModel
