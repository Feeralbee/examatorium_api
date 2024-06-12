from didiator import CommandHandler

from domain.entities import DisciplineDomainEntity
from domain.mapping import IClassMapper
from domain.models.requests import GetDisciplineRequest, GetDisciplineListRequest
from infrastructure.repositories import DisciplineRepository


class GetDisciplineHandler(CommandHandler[GetDisciplineRequest, DisciplineDomainEntity]):
    def __init__(
            self, repo: DisciplineRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: GetDisciplineRequest) -> DisciplineDomainEntity | None:
        response = await self.repo.get(command.id)
        if response:
            return self.mapper.map(DisciplineDomainEntity, response)


class GetDisciplineListHandler(CommandHandler[GetDisciplineListRequest, list[DisciplineDomainEntity]]):
    def __init__(
            self, repo: DisciplineRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: GetDisciplineListRequest) -> list[DisciplineDomainEntity]:
        disciplines = await self.repo.all(with_unique=True)
        disciplines = [self.mapper.map(DisciplineDomainEntity, i) for i in disciplines]
        return disciplines
