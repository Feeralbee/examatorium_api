from typing import Literal

from didiator import Command
from pydantic import BaseModel


class DeleteQualificationCompetenceRequest(BaseModel, Command[Literal[True]]):
    id: str
