from typing import Literal

from didiator import Command
from pydantic import BaseModel


class DeleteExamRequest(BaseModel, Command[Literal[True]]):
    id: str
