from didiator import CommandHandler

from domain.entities import QualificationCompetenceDomainEntity
from domain.mapping import IClassMapper
from domain.models.requests import GetQualCompetenciesByCompetenceIdRequest, GetQualCompetenciesByQualificationIdRequest
from infrastructure.repositories import QualificationCompetenceRepository


class GetQualCompetenciesByCompetenceIdHandler(
    CommandHandler[GetQualCompetenciesByCompetenceIdRequest,
    list[QualificationCompetenceDomainEntity]]
):
    def __init__(
            self, repo: QualificationCompetenceRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: GetQualCompetenciesByCompetenceIdRequest) -> list[QualificationCompetenceDomainEntity]:
        response = await self.repo.get_by(competence_id=command.competence_id, is_many=True)
        response = [self.mapper.map(QualificationCompetenceDomainEntity, i) for i in response]
        return response


class GetQualCompetenciesByQualificationIdHandler(
    CommandHandler[GetQualCompetenciesByQualificationIdRequest,
    list[QualificationCompetenceDomainEntity]]
):
    def __init__(
            self, repo: QualificationCompetenceRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: GetQualCompetenciesByQualificationIdRequest) -> list[QualificationCompetenceDomainEntity]:
        response = await self.repo.get_by(qualification_id=command.qualification_id, is_many=True)
        response = [self.mapper.map(QualificationCompetenceDomainEntity, i) for i in response]
        return response
