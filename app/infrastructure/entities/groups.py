from sqlalchemy import String, UUID, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from .base import BaseModel


class GroupModel(BaseModel):
    __tablename__ = 'groups'

    name: Mapped[str] = mapped_column(String, nullable=False)
    qualification_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("qualifications.id"), nullable=False,)


    def __repr__(self):
        return f'<GroupModel ' \
               f'id={self.id} ' \
               f'name={self.name} ' \
               f'qualification_id={self.qualification_id} ' \
               f'>'
