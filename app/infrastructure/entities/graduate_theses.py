from sqlalchemy import UUID, ForeignKey, Integer
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .base import BaseModel


class GraduateThesisModel(BaseModel):
    __tablename__ = 'graduate_theses'

    group_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("groups.id", ondelete="CASCADE"),
                                          nullable=False, )
    group: Mapped["GroupModel"] = relationship("GroupModel", lazy="joined", )
