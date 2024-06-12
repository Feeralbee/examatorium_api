from didiator import CommandHandler
from domain.entities import QuestionDomainEntity
from domain.mapping import IClassMapper
from domain.models.requests import UpdateQuestionRequest
from infrastructure.repositories import QuestionRepository


class UpdateQuestionHandler(CommandHandler[UpdateQuestionRequest, QuestionDomainEntity]):
    def __init__(
            self, repo: QuestionRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: UpdateQuestionRequest) -> QuestionDomainEntity:
        response = await self.repo.update(
            command.id,
            **command.model_dump(exclude={"id", }, exclude_unset=True)
        )
        return self.mapper.map(QuestionDomainEntity, response)
