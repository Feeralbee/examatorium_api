from didiator import CommandHandler

from domain.entities import QualificationDomainEntity
from domain.mapping import IClassMapper
from domain.models.requests import CreateQualificationRequest
from infrastructure.entities import QualificationModel
from infrastructure.repositories import QualificationRepository


class CreateQualificationHandler(CommandHandler[CreateQualificationRequest, QualificationDomainEntity]):
    def __init__(
            self, repo: QualificationRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: CreateQualificationRequest) -> QualificationDomainEntity:
        entity = self.mapper.map(QualificationModel, command)
        response = await self.repo.create(entity)
        return self.mapper.map(QualificationDomainEntity, response)
