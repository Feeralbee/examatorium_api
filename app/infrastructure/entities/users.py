from sqlalchemy import String, Boolean, Enum
from sqlalchemy.orm import mapped_column, Mapped

from .base import BaseModel
from ..enums import UserRoles


class UserModel(BaseModel):
    __tablename__ = 'users'

    login: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    surname: Mapped[str] = mapped_column(String, nullable=False)
    patronymic: Mapped[str] = mapped_column(String, nullable=True,)
    role: Mapped[str] = mapped_column(Enum(UserRoles), nullable=False, )
    is_blocked: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")
    password: Mapped[str] = mapped_column(String, nullable=False)

    def __repr__(self):
        return f'<UserModel ' \
               f'id={self.id} ' \
               f'login={self.login} ' \
               f'name={self.name} ' \
               f'surname={self.surname} ' \
               f'patronymic={self.patronymic} ' \
               f'role={self.role} ' \
               f'is_blocked={self.is_blocked} ' \
               f'password={self.password} ' \
               f'>'

