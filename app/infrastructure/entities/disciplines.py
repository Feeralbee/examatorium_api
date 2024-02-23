from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

from .base import BaseModel


class DisciplineModel(BaseModel):
    __tablename__ = 'disciplines'

    name: Mapped[str] = mapped_column(String, nullable=False)
    index: Mapped[str] = mapped_column(String, nullable=False)


    def __repr__(self):
        return f'<DisciplineModel ' \
               f'id={self.id} ' \
               f'name={self.name} ' \
               f'index={self.index} ' \
               f'>'

