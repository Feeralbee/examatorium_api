from sqlalchemy import UUID, ForeignKey, Integer
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .base import BaseModel


class ExamModel(BaseModel):
    __tablename__ = 'exams'

    discipline_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("disciplines.id", ondelete="CASCADE"),
                                               nullable=False, )
    discipline: Mapped["DisciplineModel"] = relationship("DisciplineModel", lazy="joined", )
    teacher_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("users.id", ondelete="CASCADE"),
                                            nullable=False, )
    teacher: Mapped["UserModel"] = relationship("UserModel", lazy="joined", )
    group_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("groups.id", ondelete="CASCADE"),
                                          nullable=False, )
    group: Mapped["GroupModel"] = relationship("GroupModel", lazy="joined", )
    semester: Mapped[int] = mapped_column(Integer, nullable=False, )
    themes: Mapped[list["ThemeModel"]] = relationship("ThemeModel", lazy="joined", cascade="all, delete")
