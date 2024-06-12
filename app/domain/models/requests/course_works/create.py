from didiator import Command
from pydantic import BaseModel

from domain.entities import CourseWorkDomainEntity


class CreateCourseWorkRequest(BaseModel, Command[CourseWorkDomainEntity]):

    discipline_id: str
    teacher_id: str
    group_id: str
