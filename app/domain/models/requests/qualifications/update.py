from didiator import Command
from pydantic import BaseModel

from domain.entities import QualificationDomainEntity


class UpdateQualificationRequest(BaseModel, Command[QualificationDomainEntity]):

    id: str
    index: str
    name: str
