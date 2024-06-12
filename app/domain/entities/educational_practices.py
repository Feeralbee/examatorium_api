from .base import BaseEntity
from .disciplines import DisciplineDomainEntity
from .users import UserDomainEntity
from .groups import GroupDomainEntity


class EducationalPracticeDomainEntity(BaseEntity):

    teacher_id: str
    teacher: UserDomainEntity
    group_id: str
    group: GroupDomainEntity
    name: str
    hours_count: int
