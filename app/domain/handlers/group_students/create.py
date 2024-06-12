from didiator import CommandHandler
from loguru import logger

from domain.entities import GroupStudentDomainEntity
from domain.mapping import IClassMapper
from domain.models.requests import CreateGroupStudentRequest
from infrastructure.entities import GroupStudentModel
from infrastructure.repositories import GroupStudentRepository


class CreateGroupStudentHandler(CommandHandler[CreateGroupStudentRequest, GroupStudentDomainEntity]):
    def __init__(
            self, repo: GroupStudentRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: CreateGroupStudentRequest) -> GroupStudentDomainEntity:
        entity = self.mapper.map(GroupStudentModel, command)
        response = await self.repo.create(entity)
        return self.mapper.map(GroupStudentDomainEntity, response)
