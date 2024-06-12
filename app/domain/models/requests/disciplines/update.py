from didiator import Command
from pydantic import BaseModel

from domain.entities import DisciplineDomainEntity


class UpdateDisciplineRequest(BaseModel, Command[DisciplineDomainEntity]):

    id: str
    name: str
    index: str
