from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from .base import BaseModel


class QualificationCompetenceModel(BaseModel):
    __tablename__ = 'qualification_competencies'

    qualification_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("qualifications.id"),
                                                  nullable=False, )
    competencies_id: Mapped[str] = mapped_column(UUID(as_uuid=False),
                                                 ForeignKey("competencies.id"),
                                                 nullable=False, )

    def __repr__(self):
        return f'<QualificationCompetenceModel ' \
               f'id={self.id} ' \
               f'qualification_id={self.qualification_id} ' \
               f'competencies_id={self.competencies_id} ' \
               f'>'
