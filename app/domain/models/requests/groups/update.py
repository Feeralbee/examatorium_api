from didiator import Command
from pydantic import BaseModel

from domain.entities import GroupDomainEntity


class UpdateGroupRequest(BaseModel, Command[GroupDomainEntity]):

    id: str
    name: str | None = None
    qualification_id: str | None = None
    speciality: str
