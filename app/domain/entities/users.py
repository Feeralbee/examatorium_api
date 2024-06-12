from misc.enums import UserRoles
from .base import BaseEntity


class UserDomainEntity(BaseEntity):
    login: str
    name: str
    surname: str
    patronymic: str | None = None
    role: UserRoles
    is_blocked: bool
    password: str
