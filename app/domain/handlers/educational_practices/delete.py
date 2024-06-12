from typing import Literal

from didiator import CommandHandler

from domain.mapping import IClassMapper
from domain.models.requests import DeleteEducationalPracticeRequest
from infrastructure.repositories import EducationalPracticeRepository


class DeleteEducationalPracticeHandler(CommandHandler[DeleteEducationalPracticeRequest, Literal[True]]):
    def __init__(
            self, repo: EducationalPracticeRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: DeleteEducationalPracticeRequest) -> Literal[True]:
        response = await self.repo.direct_delete(command.id)
        return response
