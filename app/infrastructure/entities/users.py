from sqlalchemy import String, Boolean, Enum
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .base import BaseModel
from misc.enums import UserRoles


class UserModel(BaseModel):
    __tablename__ = 'users'

    login: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    surname: Mapped[str] = mapped_column(String, nullable=False)
    patronymic: Mapped[str] = mapped_column(String, nullable=True,)
    role: Mapped[str] = mapped_column(Enum(UserRoles), nullable=False, )
    is_blocked: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")
    password: Mapped[str] = mapped_column(String, nullable=False)
    group = relationship("GroupStudentModel", lazy="joined", cascade="all, delete")
    exams = relationship("ExamModel", lazy="joined", cascade="all, delete")
    # qual_exams = relationship("QualificationExamModel", lazy="joined", cascade="all, delete")
