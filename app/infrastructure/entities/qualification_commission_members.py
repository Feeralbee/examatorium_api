from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

from .base import BaseModel


class QualificationCommissionMemberModel(BaseModel):
    __tablename__ = 'qualification_commission_members'

    name: Mapped[str] = mapped_column(String, nullable=False)
    surname: Mapped[str] = mapped_column(String, nullable=False)
    patronymic: Mapped[str] = mapped_column(String, nullable=True)

    def __repr__(self):
        return f'<QualificationCommissionMemberModel ' \
               f'id={self.id} ' \
               f'name={self.name} ' \
               f'surname={self.surname} ' \
               f'patronymic={self.patronymic} ' \
               f'>'
