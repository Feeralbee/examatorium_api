from .base import BaseRepository
from ..entities import QualificationExamsMemberModel


class QualificationExamsMemberRepository(BaseRepository[QualificationExamsMemberModel]):
    model = QualificationExamsMemberModel
