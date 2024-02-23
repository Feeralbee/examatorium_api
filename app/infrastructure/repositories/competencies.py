from .base import BaseRepository
from ..entities import CompetenceModel


class CompetenceRepository(BaseRepository[CompetenceModel]):
    model = CompetenceModel
