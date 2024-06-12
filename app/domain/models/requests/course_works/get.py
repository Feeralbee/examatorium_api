from didiator import Command
from pydantic import BaseModel

from domain.entities import CourseWorkDomainEntity


class GetCourseWorkRequest(BaseModel, Command[CourseWorkDomainEntity]):
    id: str


class GetCourseWorkListByGroupRequest(BaseModel, Command[list[CourseWorkDomainEntity]]):
    group_id: str


class GetCourseWorkListRequest(BaseModel, Command[list[CourseWorkDomainEntity]]):
    pass
