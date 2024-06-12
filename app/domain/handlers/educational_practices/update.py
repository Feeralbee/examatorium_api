from didiator import CommandHandler
from domain.entities import EducationalPracticeDomainEntity
from domain.mapping import IClassMapper
from domain.models.requests import UpdateEducationalPracticeRequest
from infrastructure.repositories import EducationalPracticeRepository


class UpdateEducationalPracticeHandler(CommandHandler[UpdateEducationalPracticeRequest, EducationalPracticeDomainEntity]):
    def __init__(
            self, repo: EducationalPracticeRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: UpdateEducationalPracticeRequest) -> EducationalPracticeDomainEntity:
        response = await self.repo.update(
            command.id,
            **command.model_dump(exclude={"id", }, exclude_unset=True)
        )
        return self.mapper.map(EducationalPracticeDomainEntity, response)
