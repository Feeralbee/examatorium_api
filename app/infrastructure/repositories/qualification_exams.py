from .base import BaseRepository
from ..entities import QualificationExamModel


class QualificationExamRepository(BaseRepository[QualificationExamModel]):
    model = QualificationExamModel
