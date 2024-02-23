from .base import BaseRepository
from ..entities import QuestionModel


class QuestionRepository(BaseRepository[QuestionModel]):
    model = QuestionModel
