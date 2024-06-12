from didiator import Command
from pydantic import BaseModel

from domain.entities import CompetenceDomainEntity


class GetCompetenceRequest(BaseModel, Command[CompetenceDomainEntity]):
    id: str


class GetCompetenceListRequest(BaseModel, Command[list[CompetenceDomainEntity]]):
    pass
