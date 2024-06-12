from sqlalchemy import String, UUID, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .base import BaseModel


class ThemeModel(BaseModel):
    __tablename__ = 'themes'

    name: Mapped[str] = mapped_column(String, nullable=False)
    exam_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("exams.id", ondelete="CASCADE"),
                                         nullable=False, )
    exam: Mapped["ExamModel"] = relationship("ExamModel", lazy="joined", )
    questions: Mapped[list["QuestionModel"]] = relationship("QuestionModel", lazy="joined", cascade="all, delete")
