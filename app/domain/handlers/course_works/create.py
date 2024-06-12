from didiator import CommandHandler

from domain.entities import CourseWorkDomainEntity
from domain.mapping import IClassMapper
from domain.models.requests import CreateCourseWorkRequest
from infrastructure.entities import CourseWorkModel
from infrastructure.repositories import CourseWorkRepository


class CreateCourseWorkHandler(CommandHandler[CreateCourseWorkRequest, CourseWorkDomainEntity]):
    def __init__(
            self, repo: CourseWorkRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: CreateCourseWorkRequest) -> CourseWorkDomainEntity:
        entity = self.mapper.map(CourseWorkModel, command)
        response = await self.repo.create(entity)
        return self.mapper.map(CourseWorkDomainEntity, response)
