from typing import Literal

from didiator import CommandHandler

from domain.mapping import IClassMapper
from domain.models.requests import DeleteGroupRequest
from infrastructure.repositories import GroupRepository


class DeleteGroupHandler(CommandHandler[DeleteGroupRequest, Literal[True]]):
    def __init__(
            self, repo: GroupRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: DeleteGroupRequest) -> Literal[True]:
        response = await self.repo.direct_delete(command.id)
        return response
