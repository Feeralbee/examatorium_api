from didiator import CommandHandler

from domain.entities import DisciplineDomainEntity
from domain.mapping import IClassMapper
from domain.models.requests import CreateDisciplineRequest
from infrastructure.entities import DisciplineModel
from infrastructure.repositories import DisciplineRepository


class CreateDisciplineHandler(CommandHandler[CreateDisciplineRequest, DisciplineDomainEntity]):
    def __init__(
            self, repo: DisciplineRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: CreateDisciplineRequest) -> DisciplineDomainEntity:
        entity = self.mapper.map(DisciplineModel, command)
        response = await self.repo.create(entity)
        return self.mapper.map(DisciplineDomainEntity, response)
