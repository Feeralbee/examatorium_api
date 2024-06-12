from didiator import Command
from pydantic import BaseModel

from domain.entities import GroupDomainEntity


class CreateGroupRequest(BaseModel, Command[GroupDomainEntity]):
    name: str
    qualification_id: str
    speciality: str
