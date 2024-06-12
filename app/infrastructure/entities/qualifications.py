from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .base import BaseModel


class QualificationModel(BaseModel):
    __tablename__ = 'qualifications'

    index: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    competencies: Mapped[list["CompetenceModel"]] = relationship("CompetenceModel", lazy="joined",
                                                                 secondary="qualification_competencies")
    groups = relationship("GroupModel", lazy="joined", cascade="all, delete")
