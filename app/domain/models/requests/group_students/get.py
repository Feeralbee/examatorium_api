from didiator import Command
from pydantic import BaseModel

from domain.entities import GroupStudentDomainEntity


class GetGroupStudentRequest(BaseModel, Command[GroupStudentDomainEntity]):
    id: str


class GetStudentGroupRequest(BaseModel, Command[GroupStudentDomainEntity]):
    student_id: str | None


class GetGroupStudentListRequest(BaseModel, Command[list[GroupStudentDomainEntity]]):
    pass
