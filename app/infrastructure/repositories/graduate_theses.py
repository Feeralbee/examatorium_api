from .base import BaseRepository
from ..entities import GraduateThesisModel


class GraduateThesisRepository(BaseRepository[GraduateThesisModel]):
    model = GraduateThesisModel
