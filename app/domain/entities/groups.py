from .users import UserDomainEntity
from .qualifications import QualificationDomainEntity
from .base import BaseEntity


class GroupDomainEntity(BaseEntity):

    name: str
    qualification_id: str
    students: list[UserDomainEntity]
    qualification: QualificationDomainEntity
    speciality: str
