from .base import BaseRepository
from ..entities import CourseWorkModel


class CourseWorkRepository(BaseRepository[CourseWorkModel]):
    model = CourseWorkModel
