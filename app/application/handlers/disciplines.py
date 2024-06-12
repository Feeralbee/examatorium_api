from typing import Annotated

from didiator import Mediator
from fastapi import APIRouter, Depends

from application.dependencies import get_mediator
from domain.entities import DisciplineDomainEntity
from domain.models.requests import disciplines

router = APIRouter(tags=["disciplines"])


@router.get("/disciplines/all")
async def all(mediator: Annotated[Mediator, Depends(get_mediator)]) -> list[DisciplineDomainEntity]:
    response = await mediator.send(disciplines.GetDisciplineListRequest())
    return response


@router.get("/disciplines/{discipline_id}")
async def discipline(discipline_id: str,
                     mediator: Annotated[Mediator, Depends(get_mediator)]) -> DisciplineDomainEntity:
    response = await mediator.send(disciplines.GetDisciplineRequest(id=discipline_id))
    return response


@router.post("/disciplines")
async def create(
        data: disciplines.CreateDisciplineRequest,
        mediator: Annotated[Mediator, Depends(get_mediator)]
) -> DisciplineDomainEntity:
    response = await mediator.send(data)
    return response


@router.patch("/disciplines")
async def update(
        data: disciplines.UpdateDisciplineRequest,
        mediator: Annotated[Mediator, Depends(get_mediator)]
) -> DisciplineDomainEntity:
    response = await mediator.send(data)
    return response


@router.delete("/disciplines/{discipline_id}")
async def delete(discipline_id: str, mediator: Annotated[Mediator, Depends(get_mediator)]):
    response = await mediator.send(disciplines.DeleteDisciplineRequest(id=discipline_id))
    return response
