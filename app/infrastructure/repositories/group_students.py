from .base import BaseRepository
from ..entities import GroupStudentModel


class GroupStudentRepository(BaseRepository[GroupStudentModel]):
    model = GroupStudentModel
