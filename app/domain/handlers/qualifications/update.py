from didiator import CommandHandler
from domain.entities import QualificationDomainEntity
from domain.mapping import IClassMapper
from domain.models.requests import UpdateQualificationRequest
from infrastructure.repositories import QualificationRepository


class UpdateQualificationHandler(CommandHandler[UpdateQualificationRequest, QualificationDomainEntity]):
    def __init__(
            self, repo: QualificationRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: UpdateQualificationRequest) -> QualificationDomainEntity:
        response = await self.repo.update(
            command.id,
            **command.model_dump(exclude={"id", }, exclude_unset=True)
        )
        return self.mapper.map(QualificationDomainEntity, response)
