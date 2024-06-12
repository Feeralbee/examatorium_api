from didiator import Command
from pydantic import BaseModel

from domain.entities import QualificationDomainEntity


class GetQualificationRequest(BaseModel, Command[QualificationDomainEntity]):
    id: str


class GetQualificationListRequest(BaseModel, Command[list[QualificationDomainEntity]]):
    pass
