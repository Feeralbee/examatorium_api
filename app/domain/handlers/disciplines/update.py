from didiator import CommandHandler
from domain.entities import DisciplineDomainEntity
from domain.mapping import IClassMapper
from domain.models.requests import UpdateDisciplineRequest
from infrastructure.repositories import DisciplineRepository


class UpdateDisciplineHandler(CommandHandler[UpdateDisciplineRequest, DisciplineDomainEntity]):
    def __init__(
            self, repo: DisciplineRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: UpdateDisciplineRequest) -> DisciplineDomainEntity:
        response = await self.repo.update(
            command.id,
            **command.model_dump(exclude={"id", }, exclude_unset=True)
        )
        return self.mapper.map(DisciplineDomainEntity, response)
