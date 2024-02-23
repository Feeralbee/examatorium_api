from .base import BaseRepository
from ..entities import ExamModel


class ExamRepository(BaseRepository[ExamModel]):
    model = ExamModel
