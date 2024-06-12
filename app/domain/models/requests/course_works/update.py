from didiator import Command
from pydantic import BaseModel

from domain.entities import CourseWorkDomainEntity


class UpdateCourseWorkRequest(BaseModel, Command[CourseWorkDomainEntity]):

    id: str
    discipline_id: str | None = None
    teacher_id: str | None = None
    group_id: str | None = None
