from didiator import CommandHandler

from domain.entities import EducationalPracticeDomainEntity
from domain.mapping import IClassMapper
from domain.models.requests import GetEducationalPracticeRequest, GetEducationalPracticeListRequest, \
    GetEducationalPracticeListByGroupRequest
from infrastructure.repositories import EducationalPracticeRepository


class GetEducationalPracticeHandler(CommandHandler[GetEducationalPracticeRequest, EducationalPracticeDomainEntity]):
    def __init__(
            self, repo: EducationalPracticeRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: GetEducationalPracticeRequest) -> EducationalPracticeDomainEntity | None:
        response = await self.repo.get(command.id)
        if response:
            return self.mapper.map(EducationalPracticeDomainEntity, response)


class GetEducationalPracticeListByGroupHandler(
    CommandHandler[GetEducationalPracticeListByGroupRequest, list[EducationalPracticeDomainEntity]]):
    def __init__(
            self, repo: EducationalPracticeRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: GetEducationalPracticeListByGroupRequest) -> list[
        EducationalPracticeDomainEntity]:
        response = await self.repo.get_by(group_id=command.group_id, is_many=True, with_unique=True)
        response = [self.mapper.map(EducationalPracticeDomainEntity, i) for i in response]
        return response


class GetEducationalPracticeListHandler(
    CommandHandler[GetEducationalPracticeListRequest, list[EducationalPracticeDomainEntity]]):
    def __init__(
            self, repo: EducationalPracticeRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: GetEducationalPracticeListRequest) -> list[EducationalPracticeDomainEntity]:
        educational_practice = await self.repo.all(with_unique=True)
        educational_practice = [self.mapper.map(EducationalPracticeDomainEntity, i) for i in educational_practice]
        return educational_practice
