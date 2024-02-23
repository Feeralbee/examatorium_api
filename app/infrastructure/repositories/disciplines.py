from .base import BaseRepository
from ..entities import DisciplineModel


class DisciplineRepository(BaseRepository[DisciplineModel]):
    model = DisciplineModel
