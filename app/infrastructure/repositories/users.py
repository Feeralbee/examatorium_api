from .base import BaseRepository
from sqlalchemy import select
from ..entities import UserModel


class UserRepository(BaseRepository[UserModel]):
    model = UserModel
