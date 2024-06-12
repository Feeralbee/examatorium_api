import  hashlib
from didiator import CommandHandler

from domain.entities import UserDomainEntity
from domain.mapping import IClassMapper
from domain.models.requests import CreateUserRequest
from infrastructure.entities import UserModel
from infrastructure.repositories import UserRepository


class CreateUserHandler(CommandHandler[CreateUserRequest, UserDomainEntity]):
    def __init__(
            self, repo: UserRepository,
            mapper: IClassMapper
    ):
        self.repo = repo
        self.mapper = mapper

    async def __call__(self, command: CreateUserRequest) -> UserDomainEntity:
        command.password = hashlib.md5(command.password.encode()).hexdigest()
        entity = self.mapper.map(UserModel, command)
        response = await self.repo.create(entity)
        return self.mapper.map(UserDomainEntity, response)
