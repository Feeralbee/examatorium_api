from didiator import CommandHandler

from domain.entities import GroupDomainEntity
from domain.mapping import IClassMapper
from domain.models.requests import CreateGroupRequest
from infrastructure.entities import GroupModel
from infrastructure.repositories import GroupRepository


class CreateGroupHandler(CommandHandler[CreateGroupRequest, GroupDomainEntity]):
    def __init__(
            self, repo: GroupRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: CreateGroupRequest) -> GroupDomainEntity:
        entity = self.mapper.map(GroupModel, command)
        response = await self.repo.create(entity)
        return self.mapper.map(GroupDomainEntity, response)
