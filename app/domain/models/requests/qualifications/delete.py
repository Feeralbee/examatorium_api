from typing import Literal

from didiator import Command
from pydantic import BaseModel


class DeleteQualificationRequest(BaseModel, Command[Literal[True]]):
    id: str
