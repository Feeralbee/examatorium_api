from didiator import Command
from pydantic import BaseModel

from domain.entities import UserDomainEntity


class GetUserRequest(BaseModel, Command[UserDomainEntity]):
    id: str


class GetUserByAuthorisationRequest(BaseModel, Command[UserDomainEntity]):
    login: str
    password: str


class GetUserListRequest(BaseModel, Command[list[UserDomainEntity]]):
    pass
