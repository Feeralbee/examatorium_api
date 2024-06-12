from didiator import CommandHandler
from domain.entities import GroupDomainEntity
from domain.mapping import IClassMapper
from domain.models.requests import UpdateGroupRequest
from infrastructure.repositories import GroupRepository


class UpdateGroupHandler(CommandHandler[UpdateGroupRequest, GroupDomainEntity]):
    def __init__(
            self, repo: GroupRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: UpdateGroupRequest) -> GroupDomainEntity:
        response = await self.repo.update(
            command.id,
            **command.model_dump(exclude={"id", }, exclude_unset=True)
        )
        return self.mapper.map(GroupDomainEntity, response)
