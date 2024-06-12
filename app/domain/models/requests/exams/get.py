from didiator import Command
from pydantic import BaseModel

from domain.entities import ExamDomainEntity


class GetExamRequest(BaseModel, Command[ExamDomainEntity]):
    id: str


class GetExamListByRequest(BaseModel, Command[list[ExamDomainEntity]]):
    discipline_id: str | None = None
    teacher_id: str | None = None
    group_id: str | None = None
    semester: int | None = None


class GetExamListByTeacherRequest(BaseModel, Command[list[ExamDomainEntity]]):
    teacher_id: str


class GetExamListByGroupRequest(BaseModel, Command[list[ExamDomainEntity]]):
    group_id: str

class GetExamListRequest(BaseModel, Command[list[ExamDomainEntity]]):
    pass
