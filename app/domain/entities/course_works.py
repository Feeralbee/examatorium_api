from .base import BaseEntity
from .disciplines import DisciplineDomainEntity
from .users import UserDomainEntity
from .groups import GroupDomainEntity


class CourseWorkDomainEntity(BaseEntity):

    discipline_id: str
    discipline: DisciplineDomainEntity
    teacher_id: str
    teacher: UserDomainEntity
    group_id: str
    group: GroupDomainEntity
