from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .base import BaseModel


class DisciplineModel(BaseModel):
    __tablename__ = 'disciplines'

    name: Mapped[str] = mapped_column(String, nullable=False)
    index: Mapped[str] = mapped_column(String, nullable=False)
    exams = relationship("ExamModel", lazy="joined", cascade="all, delete")
