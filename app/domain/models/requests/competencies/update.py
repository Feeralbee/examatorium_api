from didiator import Command
from pydantic import BaseModel

from domain.entities import CompetenceDomainEntity
from misc.enums import CompetenceTypes


class UpdateCompetenceRequest(BaseModel, Command[CompetenceDomainEntity]):
    id: str
    name: str
    type: CompetenceTypes
    index: str
