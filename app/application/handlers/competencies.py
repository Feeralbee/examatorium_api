from typing import Annotated

from didiator import Mediator
from fastapi import APIRouter, Depends

from application.dependencies import get_mediator
from domain.entities import CompetenceDomainEntity
from domain.models.requests import competencies, GetQualCompetenciesByCompetenceIdRequest, \
    DeleteQualificationCompetenceRequest

router = APIRouter(tags=["competencies"])


@router.get("/competencies/all")
async def all(mediator: Annotated[Mediator, Depends(get_mediator)]) -> list[CompetenceDomainEntity]:
    response = await mediator.send(competencies.GetCompetenceListRequest())
    return response


@router.get("/competencies/{competence_id}")
async def competence(competence_id: str,
                     mediator: Annotated[Mediator, Depends(get_mediator)]) -> CompetenceDomainEntity:
    response = await mediator.send(competencies.GetCompetenceRequest(id=competence_id))
    return response


@router.post("/competencies")
async def create(
        data: competencies.CreateCompetenceRequest,
        mediator: Annotated[Mediator, Depends(get_mediator)]
) -> CompetenceDomainEntity:
    response = await mediator.send(data)
    return response


@router.patch("/competencies")
async def update(
        data: competencies.UpdateCompetenceRequest,
        mediator: Annotated[Mediator, Depends(get_mediator)]
) -> CompetenceDomainEntity:
    response = await mediator.send(data)
    return response


@router.delete("/competencies/{competence_id}")
async def delete(competence_id: str, mediator: Annotated[Mediator, Depends(get_mediator)]):
    qualifications_competencies = await mediator.send(
        GetQualCompetenciesByCompetenceIdRequest(competence_id=competence_id))
    for qualification_competence in qualifications_competencies:
        await mediator.send(DeleteQualificationCompetenceRequest(id=qualification_competence.id))
    response = await mediator.send(competencies.DeleteCompetenceRequest(id=competence_id))
    return response
