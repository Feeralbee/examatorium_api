from didiator import CommandHandler

from domain.entities import GroupDomainEntity
from domain.mapping import IClassMapper
from domain.models.requests import GetGroupRequest, GetGroupListRequest
from infrastructure.repositories import GroupRepository


class GetGroupHandler(CommandHandler[GetGroupRequest, GroupDomainEntity]):
    def __init__(
            self, repo: GroupRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: GetGroupRequest) -> GroupDomainEntity | None:
        groups = await self.repo.get(command.id)
        if groups:
            groups = self.mapper.map(GroupDomainEntity, groups)
            groups.students = [student.copy(exclude={"password",}) for student in groups.students]
            return groups


class GetGroupListHandler(CommandHandler[GetGroupListRequest, list[GroupDomainEntity]]):
    def __init__(
            self, repo: GroupRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: GetGroupListRequest) -> list[GroupDomainEntity]:
        groups = await self.repo.all(with_unique=True)
        groups = [self.mapper.map(GroupDomainEntity, i) for i in groups]
        for group in groups:
            for student in group.students:
                del student.password
        return groups
