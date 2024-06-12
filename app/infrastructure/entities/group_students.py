from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from .base import BaseModel


class GroupStudentModel(BaseModel):
    __tablename__ = 'group_students'

    student_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("users.id", ondelete="CASCADE"),
                                            nullable=False, unique=True, )
    group_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("groups.id", ondelete="CASCADE"),
                                          nullable=False, )
