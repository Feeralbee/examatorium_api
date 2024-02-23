from .base import BaseRepository
from ..entities import QualificationModel


class QualificationRepository(BaseRepository[QualificationModel]):
    model = QualificationModel
