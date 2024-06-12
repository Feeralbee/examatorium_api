from typing import Literal

from didiator import Command
from pydantic import BaseModel


class DeleteGroupStudentRequest(BaseModel, Command[Literal[True]]):
    id: str


class DeleteGroupStudentByStudentIdRequest(BaseModel, Command[Literal[True]]):
    student_id: str
