from didiator import CommandHandler

from domain.entities import CompetenceDomainEntity
from domain.mapping import IClassMapper
from domain.models.requests import GetCompetenceRequest, GetCompetenceListRequest
from infrastructure.repositories import CompetenceRepository


class GetCompetenceHandler(CommandHandler[GetCompetenceRequest, CompetenceDomainEntity]):
    def __init__(
            self, repo: CompetenceRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: GetCompetenceRequest) -> CompetenceDomainEntity | None:
        response = await self.repo.get(command.id)
        if response:
            return self.mapper.map(CompetenceDomainEntity, response)


class GetCompetenceListHandler(CommandHandler[GetCompetenceListRequest, list[CompetenceDomainEntity]]):
    def __init__(
            self, repo: CompetenceRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: GetCompetenceListRequest) -> list[CompetenceDomainEntity]:
        competencies = await self.repo.all()
        competencies = [self.mapper.map(CompetenceDomainEntity, i) for i in competencies]
        return competencies
