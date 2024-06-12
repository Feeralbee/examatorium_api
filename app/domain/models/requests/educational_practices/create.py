from didiator import Command
from pydantic import BaseModel

from domain.entities import EducationalPracticeDomainEntity


class CreateEducationalPracticeRequest(BaseModel, Command[EducationalPracticeDomainEntity]):
    teacher_id: str
    group_id: str
    name: str
    hours_count: int
