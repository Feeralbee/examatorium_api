from sqlalchemy import String, UUID, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from .base import BaseModel


class ThemeModel(BaseModel):
    __tablename__ = 'themes'

    name: Mapped[str] = mapped_column(String, nullable=False)
    discipline_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("disciplines.id"), nullable=False, )


    def __repr__(self):
        return f'<ThemeModel ' \
               f'id={self.id} ' \
               f'name={self.name} ' \
               f'discipline_id={self.discipline_id} ' \
               f'>'

