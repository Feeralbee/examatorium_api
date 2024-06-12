from didiator import Command
from pydantic import BaseModel

from domain.entities import GroupDomainEntity


class GetGroupRequest(BaseModel, Command[GroupDomainEntity]):
    id: str


class GetGroupListRequest(BaseModel, Command[list[GroupDomainEntity]]):
    pass
