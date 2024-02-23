from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

from .base import BaseModel


class QualificationModel(BaseModel):
    __tablename__ = 'qualifications'

    index: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)


    def __repr__(self):
        return f'<QualificationModel ' \
               f'id={self.id} ' \
               f'index={self.index} ' \
               f'name={self.name} ' \
               f'>'

