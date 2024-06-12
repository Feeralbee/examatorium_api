from didiator import Command
from pydantic import BaseModel

from domain.entities import CompetenceDomainEntity
from misc.enums import CompetenceTypes


class CreateCompetenceRequest(BaseModel, Command[CompetenceDomainEntity]):

    name: str
    type: CompetenceTypes
    index: str
