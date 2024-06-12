from didiator import Command
from pydantic import BaseModel

from domain.entities import DisciplineDomainEntity


class CreateDisciplineRequest(BaseModel, Command[DisciplineDomainEntity]):

    name: str
    index: str
