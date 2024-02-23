from sqlalchemy import String, Enum
from sqlalchemy.orm import mapped_column, Mapped
from ..enums import CompetenceTypes
from .base import BaseModel


class CompetenceModel(BaseModel):
    __tablename__ = 'competencies'

    name: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[str] = mapped_column(Enum(CompetenceTypes), nullable=False)
    index: Mapped[str] = mapped_column(String, nullable=False)

    def __repr__(self):
        return f'<CompetenceModel ' \
               f'id={self.id} ' \
               f'name={self.name} ' \
               f'type={self.type} ' \
               f'index={self.index} ' \
               f'>'

