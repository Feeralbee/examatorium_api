from didiator import Command
from pydantic import BaseModel

from domain.entities import ThemeDomainEntity


class UpdateThemeRequest(BaseModel, Command[ThemeDomainEntity]):

    id: str
    name: str
    exam_id: str
