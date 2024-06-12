from didiator import Command
from pydantic import BaseModel

from domain.entities import ThemeDomainEntity


class CreateThemeRequest(BaseModel, Command[ThemeDomainEntity]):
    name: str
    exam_id: str
