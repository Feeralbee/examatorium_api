from didiator import Command
from pydantic import BaseModel

from domain.entities import DisciplineDomainEntity


class GetDisciplineRequest(BaseModel, Command[DisciplineDomainEntity]):
    id: str


class GetDisciplineListRequest(BaseModel, Command[list[DisciplineDomainEntity]]):
    pass
