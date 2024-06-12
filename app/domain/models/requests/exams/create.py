from didiator import Command
from pydantic import BaseModel

from domain.entities import ExamDomainEntity


class CreateExamRequest(BaseModel, Command[ExamDomainEntity]):
    discipline_id: str
    teacher_id: str
    group_id: str
    semester: int
