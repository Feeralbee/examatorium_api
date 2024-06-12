from sqlalchemy import String, Boolean, UUID, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship, backref

from .base import BaseModel


class QuestionModel(BaseModel):
    __tablename__ = 'questions'

    name: Mapped[str] = mapped_column(String, nullable=False)
    is_task_question: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")
    theme_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("themes.id", ondelete="CASCADE"),
                                          nullable=False, )
