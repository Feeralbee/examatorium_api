from didiator import CommandHandler

from domain.entities import QualificationCompetenceDomainEntity
from domain.mapping import IClassMapper
from domain.models.requests import CreateQualificationCompetenceRequest
from infrastructure.entities import QualificationCompetenceModel
from infrastructure.repositories import QualificationCompetenceRepository


class CreateQualificationCompetenceHandler(
    CommandHandler[CreateQualificationCompetenceRequest, QualificationCompetenceDomainEntity]):
    def __init__(
            self, repo: QualificationCompetenceRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: CreateQualificationCompetenceRequest) -> QualificationCompetenceDomainEntity:
        entity = self.mapper.map(QualificationCompetenceModel, command)
        response = await self.repo.create(entity)
        return self.mapper.map(QualificationCompetenceDomainEntity, response)
