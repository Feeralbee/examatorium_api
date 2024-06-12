from didiator import Command
from pydantic import BaseModel

from domain.entities import GraduateThesisDomainEntity


class UpdateGraduateThesisRequest(BaseModel, Command[GraduateThesisDomainEntity]):

    id: str
    group_id: str | None = None
