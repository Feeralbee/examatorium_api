from didiator import Command
from pydantic import BaseModel

from domain.entities import UserDomainEntity
from misc.enums import UserRoles


class CreateUserRequest(BaseModel, Command[UserDomainEntity]):
    login: str
    name: str
    surname: str
    patronymic: str | None = None
    role: UserRoles
    password: str
