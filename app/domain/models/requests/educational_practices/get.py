from didiator import Command
from pydantic import BaseModel

from domain.entities import EducationalPracticeDomainEntity


class GetEducationalPracticeRequest(BaseModel, Command[EducationalPracticeDomainEntity]):
    id: str


class GetEducationalPracticeListByGroupRequest(BaseModel, Command[list[EducationalPracticeDomainEntity]]):
    group_id: str


class GetEducationalPracticeListRequest(BaseModel, Command[list[EducationalPracticeDomainEntity]]):
    pass
