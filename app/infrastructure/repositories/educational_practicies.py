from .base import BaseRepository
from ..entities import EducationalPracticeModel


class EducationalPracticeRepository(BaseRepository[EducationalPracticeModel]):
    model = EducationalPracticeModel
