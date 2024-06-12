from sqlalchemy import String, Enum
from sqlalchemy.orm import mapped_column, Mapped, relationship
from misc.enums import CompetenceTypes
from .base import BaseModel


class CompetenceModel(BaseModel):
    __tablename__ = 'competencies'

    name: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[str] = mapped_column(Enum(CompetenceTypes), nullable=False)
    index: Mapped[str] = mapped_column(String, nullable=False)
