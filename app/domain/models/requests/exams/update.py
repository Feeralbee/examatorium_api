from didiator import Command
from pydantic import BaseModel

from domain.entities import ExamDomainEntity


class UpdateExamRequest(BaseModel, Command[ExamDomainEntity]):

    id: str
    discipline_id: str | None = None
    teacher_id: str | None = None
    group_id: str | None = None
    semester: int | None = None
