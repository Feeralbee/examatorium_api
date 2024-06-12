from didiator import Command
from pydantic import BaseModel

from domain.entities import UserDomainEntity
from misc.enums import UserRoles


class UpdateUserRequest(BaseModel, Command[UserDomainEntity]):
    id: str
    login: str | None = None
    name: str | None = None
    surname: str | None = None
    patronymic: str | None = None
    role: UserRoles | None = None
    is_blocked: bool | None = None


class UpdateUserPasswordRequest(BaseModel, Command[UserDomainEntity]):
    id: str
    password: str
