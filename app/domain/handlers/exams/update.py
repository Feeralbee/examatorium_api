from didiator import CommandHandler
from domain.entities import ExamDomainEntity
from domain.mapping import IClassMapper
from domain.models.requests import UpdateExamRequest
from infrastructure.repositories import ExamRepository


class UpdateExamHandler(CommandHandler[UpdateExamRequest, ExamDomainEntity]):
    def __init__(
            self, repo: ExamRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: UpdateExamRequest) -> ExamDomainEntity:
        response = await self.repo.update(
            command.id,
            **command.model_dump(exclude={"id", }, exclude_unset=True)
        )
        return self.mapper.map(ExamDomainEntity, response)
