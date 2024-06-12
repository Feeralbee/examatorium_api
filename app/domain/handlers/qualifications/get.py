from didiator import CommandHandler

from domain.entities import QualificationDomainEntity
from domain.mapping import IClassMapper
from domain.models.requests import GetQualificationRequest, GetQualificationListRequest
from infrastructure.repositories import QualificationRepository


class GetQualificationHandler(CommandHandler[GetQualificationRequest, QualificationDomainEntity]):
    def __init__(
            self, repo: QualificationRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: GetQualificationRequest) -> QualificationDomainEntity | None:
        response = await self.repo.get(command.id)
        if response:
            return self.mapper.map(QualificationDomainEntity, response)


class GetQualificationListHandler(CommandHandler[GetQualificationListRequest, list[QualificationDomainEntity]]):
    def __init__(
            self, repo: QualificationRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: GetQualificationListRequest) -> list[QualificationDomainEntity]:
        qualifications = await self.repo.all(with_unique=True)
        qualifications = [self.mapper.map(QualificationDomainEntity, i) for i in qualifications]
        return qualifications
