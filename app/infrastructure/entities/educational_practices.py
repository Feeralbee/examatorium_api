from sqlalchemy import UUID, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .base import BaseModel


class EducationalPracticeModel(BaseModel):
    __tablename__ = 'educational_practices'

    teacher_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("users.id", ondelete="CASCADE"),
                                            nullable=False, )
    teacher: Mapped["UserModel"] = relationship("UserModel", lazy="joined", )
    group_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("groups.id", ondelete="CASCADE"),
                                          nullable=False, )
    group: Mapped["GroupModel"] = relationship("GroupModel", lazy="joined", )
    name: Mapped[str] = mapped_column(String, nullable=False, )
    hours_count: Mapped[int] = mapped_column(Integer, nullable=False)
