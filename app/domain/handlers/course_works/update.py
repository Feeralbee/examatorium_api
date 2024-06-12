from didiator import CommandHandler
from domain.entities import CourseWorkDomainEntity
from domain.mapping import IClassMapper
from domain.models.requests import UpdateCourseWorkRequest
from infrastructure.repositories import CourseWorkRepository


class UpdateCourseWorkHandler(CommandHandler[UpdateCourseWorkRequest, CourseWorkDomainEntity]):
    def __init__(
            self, repo: CourseWorkRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: UpdateCourseWorkRequest) -> CourseWorkDomainEntity:
        response = await self.repo.update(
            command.id,
            **command.model_dump(exclude={"id", }, exclude_unset=True)
        )
        return self.mapper.map(CourseWorkDomainEntity, response)
