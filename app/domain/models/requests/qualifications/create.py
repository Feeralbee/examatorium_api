from didiator import Command
from pydantic import BaseModel

from domain.entities import QualificationDomainEntity


class CreateQualificationRequest(BaseModel, Command[QualificationDomainEntity]):
    index: str
    name: str
