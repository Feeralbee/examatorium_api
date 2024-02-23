from sqlalchemy import String, UUID, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from .base import BaseModel


class GroupStudentModel(BaseModel):
    __tablename__ = 'group_students'

    student_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("users.id"), nullable=False, unique=True,)
    group_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("groups.id"), nullable=False,)

    def __repr__(self):
        return f'<GroupModel ' \
               f'id={self.id} ' \
               f'student_id={self.student_id} ' \
               f'group_id={self.group_id} ' \
               f'>'
