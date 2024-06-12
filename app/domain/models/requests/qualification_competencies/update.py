from didiator import Command
from pydantic import BaseModel

from domain.entities import QualificationCompetenceDomainEntity


class UpdateQualificationCompetenceRequest(BaseModel, Command[QualificationCompetenceDomainEntity]):

    id: str
    qualification_id: str
    competencies_id: str
