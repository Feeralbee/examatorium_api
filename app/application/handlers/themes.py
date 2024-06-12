from typing import Annotated

from didiator import Mediator
from fastapi import APIRouter, Depends

from application.dependencies import get_mediator
from domain.entities import ThemeDomainEntity, QuestionDomainEntity
from domain.models.requests import themes, CreateQuestionRequest, DeleteQuestionRequest

router = APIRouter(tags=["themes"])


@router.get("/themes/all")
async def all(mediator: Annotated[Mediator, Depends(get_mediator)]) -> list[ThemeDomainEntity]:
    return await mediator.send(themes.GetThemeListRequest())


@router.get("/themes/{theme_id}")
async def theme(theme_id: str, mediator: Annotated[Mediator, Depends(get_mediator)]) -> ThemeDomainEntity:
    request = themes.GetThemeRequest(id=theme_id)
    response = await mediator.send(request)
    return response


@router.post("/themes")
async def create(
        data: themes.CreateThemeRequest,
        mediator: Annotated[Mediator, Depends(get_mediator)]
) -> ThemeDomainEntity:
    response = await mediator.send(data)
    return response


@router.post("/themes/questions")
async def add_question(data: CreateQuestionRequest, mediator: Annotated[Mediator, Depends(get_mediator)]) -> QuestionDomainEntity:
    return await mediator.send(data)


@router.delete("/themes/questions")
async def delete_question(id: str, mediator: Annotated[Mediator, Depends(get_mediator)]):
    return await mediator.send(DeleteQuestionRequest(id=id))


@router.patch("/themes")
async def update(theme_data: themes.UpdateThemeRequest, mediator: Annotated[Mediator, Depends(get_mediator)]) -> ThemeDomainEntity:
    response = await mediator.send(theme_data)
    return response


@router.delete("/themes/{themes_id}")
async def delete(theme_id: str, mediator: Annotated[Mediator, Depends(get_mediator)]):
    response = await mediator.send(themes.DeleteThemeRequest(id=theme_id))
    return response
