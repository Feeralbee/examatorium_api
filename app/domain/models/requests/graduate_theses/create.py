from didiator import Command
from pydantic import BaseModel

from domain.entities import GraduateThesisDomainEntity


class CreateGraduateThesisRequest(BaseModel, Command[GraduateThesisDomainEntity]):
    group_id: str
