from didiator import Command
from pydantic import BaseModel

from domain.entities import QualificationCompetenceDomainEntity


class CreateQualificationCompetenceRequest(BaseModel, Command[QualificationCompetenceDomainEntity]):

    qualification_id: str
    competence_id: str
