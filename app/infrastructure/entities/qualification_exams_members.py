from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from .base import BaseModel


class QualificationExamsMemberModel(BaseModel):
    __tablename__ = 'qualification_exams_members'

    qualification_exam_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("qualification_exams.id"),
                                                       nullable=False, )
    commission_member_id: Mapped[str] = mapped_column(UUID(as_uuid=False),
                                                      ForeignKey("qualification_commission_members.id"),
                                                      nullable=False, )

    def __repr__(self):
        return f'<QualificationExamsMemberModel ' \
               f'id={self.id} ' \
               f'qualification_exam_id={self.qualification_exam_id} ' \
               f'commission_member_id={self.commission_member_id} ' \
               f'>'
