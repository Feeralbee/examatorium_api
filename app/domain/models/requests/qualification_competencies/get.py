from didiator import Command
from pydantic import BaseModel

from domain.entities import QualificationCompetenceDomainEntity


class GetQualificationCompetenceRequest(BaseModel, Command[QualificationCompetenceDomainEntity]):
    id: str


class GetQualCompetenciesByCompetenceIdRequest(BaseModel, Command[list[QualificationCompetenceDomainEntity]]):
    competence_id: str


class GetQualCompetenciesByQualificationIdRequest(BaseModel, Command[list[QualificationCompetenceDomainEntity]]):
    qualification_id: str


class GetQualificationCompetenceListRequest(BaseModel, Command[list[QualificationCompetenceDomainEntity]]):
    pass
