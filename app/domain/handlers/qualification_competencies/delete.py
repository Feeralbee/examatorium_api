from typing import Literal

from didiator import CommandHandler

from domain.mapping import IClassMapper
from domain.models.requests import DeleteQualificationCompetenceRequest
from infrastructure.repositories import QualificationCompetenceRepository


class DeleteQualificationCompetenceHandler(CommandHandler[DeleteQualificationCompetenceRequest, Literal[True]]):
    def __init__(
            self,
            repo: QualificationCompetenceRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: DeleteQualificationCompetenceRequest) -> Literal[True]:
        response = await self.repo.delete(command.id)
        return response
