from didiator import CommandHandler

from domain.entities import EducationalPracticeDomainEntity
from domain.mapping import IClassMapper
from domain.models.requests import CreateEducationalPracticeRequest
from infrastructure.entities import EducationalPracticeModel
from infrastructure.repositories import EducationalPracticeRepository


class CreateEducationalPracticeHandler(CommandHandler[CreateEducationalPracticeRequest, EducationalPracticeDomainEntity]):
    def __init__(
            self, repo: EducationalPracticeRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: CreateEducationalPracticeRequest) -> EducationalPracticeDomainEntity:
        entity = self.mapper.map(EducationalPracticeModel, command)
        response = await self.repo.create(entity)
        return self.mapper.map(EducationalPracticeDomainEntity, response)
