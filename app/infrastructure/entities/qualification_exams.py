from sqlalchemy import UUID, ForeignKey, Integer
from sqlalchemy.orm import mapped_column, Mapped

from .base import BaseModel


class QualificationExamModel(BaseModel):
    __tablename__ = 'qualification_exams'

    discipline_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("disciplines.id"), nullable=False, )
    teacher_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("users.id"), nullable=False, )
    group_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("groups.id"), nullable=False, )
    semester: Mapped[int] = mapped_column(Integer, nullable=False,)

    def __repr__(self):
        return f'<QualificationExamModel ' \
               f'id={self.id} ' \
               f'discipline_id={self.discipline_id} ' \
               f'teacher_id={self.teacher_id} ' \
               f'group_id={self.group_id} ' \
               f'semester={self.semester} ' \
               f'>'

