from didiator import CommandHandler

from domain.entities import GraduateThesisDomainEntity
from domain.mapping import IClassMapper
from domain.models.requests import GetGraduateThesisRequest, GetGraduateThesisListRequest, \
    GetGraduateThesisListByGroupRequest
from infrastructure.repositories import GraduateThesisRepository


class GetGraduateThesisHandler(CommandHandler[GetGraduateThesisRequest, GraduateThesisDomainEntity]):
    def __init__(
            self, repo: GraduateThesisRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: GetGraduateThesisRequest) -> GraduateThesisDomainEntity | None:
        response = await self.repo.get(command.id)
        if response:
            return self.mapper.map(GraduateThesisDomainEntity, response)


class GetGraduateThesisListByGroupHandler(
    CommandHandler[GetGraduateThesisListByGroupRequest, list[GraduateThesisDomainEntity]]):
    def __init__(
            self, repo: GraduateThesisRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: GetGraduateThesisListByGroupRequest) -> list[GraduateThesisDomainEntity]:
        response = await self.repo.get_by(group_id=command.group_id, is_many=True, with_unique=True)
        response = [self.mapper.map(GraduateThesisDomainEntity, i) for i in response]
        return response


class GetGraduateThesisListHandler(CommandHandler[GetGraduateThesisListRequest, list[GraduateThesisDomainEntity]]):
    def __init__(
            self, repo: GraduateThesisRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: GetGraduateThesisListRequest) -> list[GraduateThesisDomainEntity]:
        graduate_theses = await self.repo.all(with_unique=True)
        graduate_theses = [self.mapper.map(GraduateThesisDomainEntity, i) for i in graduate_theses]
        return graduate_theses
