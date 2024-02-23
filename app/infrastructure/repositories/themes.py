from .base import BaseRepository
from ..entities import ThemeModel


class ThemeRepository(BaseRepository[ThemeModel]):
    model = ThemeModel
