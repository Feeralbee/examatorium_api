from .base import BaseRepository
from ..entities import QualificationCommissionMemberModel


class QualificationCommissionMemberRepository(BaseRepository[QualificationCommissionMemberModel]):
    model = QualificationCommissionMemberModel
