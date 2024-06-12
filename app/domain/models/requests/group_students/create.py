from didiator import Command
from pydantic import BaseModel

from domain.entities import GroupStudentDomainEntity


class CreateGroupStudentRequest(BaseModel, Command[GroupStudentDomainEntity]):

    student_id: str
    group_id: str
