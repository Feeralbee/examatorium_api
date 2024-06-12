from typing import Literal

from didiator import CommandHandler

from domain.mapping import IClassMapper
from domain.models.requests import DeleteUserRequest
from infrastructure.repositories import UserRepository, GroupStudentRepository


class DeleteUserHandler(CommandHandler[DeleteUserRequest, Literal[True]]):
    def __init__(
            self, repo: UserRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: DeleteUserRequest) -> Literal[True]:
        response = await self.repo.direct_delete(command.id)
        return response
