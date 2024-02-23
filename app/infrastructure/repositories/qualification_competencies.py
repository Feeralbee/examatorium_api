from .base import BaseRepository
from ..entities import QualificationCompetenceModel


class QualificationCompetenceRepository(BaseRepository[QualificationCompetenceModel]):
    model = QualificationCompetenceModel
