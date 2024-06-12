from typing import Literal

from didiator import Command
from pydantic import BaseModel


class DeleteDisciplineRequest(BaseModel, Command[Literal[True]]):
    id: str
