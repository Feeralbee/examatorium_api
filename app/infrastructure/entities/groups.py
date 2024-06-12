from sqlalchemy import String, UUID, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .base import BaseModel


class GroupModel(BaseModel):
    __tablename__ = 'groups'

    name: Mapped[str] = mapped_column(String, nullable=False)
    qualification_id: Mapped[str] = mapped_column(UUID(as_uuid=False),
                                                  ForeignKey("qualifications.id", ondelete="CASCADE"),
                                                  nullable=False, )
    students: Mapped[list["UserModel"]] = relationship("UserModel", lazy="joined", secondary="group_students", )
    qualification: Mapped["QualificationModel"] = relationship(
        "QualificationModel",
        lazy="joined",
    )
    speciality: Mapped[str] = mapped_column(String, nullable=False, )
    exams = relationship("ExamModel", lazy="joined", cascade="all, delete")
