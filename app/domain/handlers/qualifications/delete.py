from typing import Literal

from didiator import CommandHandler

from domain.mapping import IClassMapper
from domain.models.requests import DeleteQualificationRequest
from infrastructure.repositories import QualificationRepository


class DeleteQualificationHandler(CommandHandler[DeleteQualificationRequest, Literal[True]]):
    def __init__(
            self, repo: QualificationRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: DeleteQualificationRequest) -> Literal[True]:
        response = await self.repo.delete(command.id)
        return response
