from didiator import Command
from pydantic import BaseModel

from domain.entities import EducationalPracticeDomainEntity


class UpdateEducationalPracticeRequest(BaseModel, Command[EducationalPracticeDomainEntity]):

    id: str
    teacher_id: str | None = None
    group_id: str | None = None
    name: str | None = None
    hours_count: int | None = None
