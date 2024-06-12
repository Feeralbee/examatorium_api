from datetime import datetime
from typing import Annotated

from didiator import Mediator
from docxtpl import DocxTemplate
from fastapi import APIRouter, Depends
from starlette.responses import FileResponse

from application.dependencies import get_mediator
from domain.entities import EducationalPracticeDomainEntity
from domain.models.requests import educational_practices, GetStudentGroupRequest, GetUserRequest

router = APIRouter(tags=["educational_practices"])


@router.get("/educational_practices/all")
async def all(mediator: Annotated[Mediator, Depends(get_mediator)]) -> list[EducationalPracticeDomainEntity]:
    response = await mediator.send(educational_practices.GetEducationalPracticeListRequest())
    return response


@router.get("/educational_practices/student")
async def student_educational_practices(student_id: str, mediator: Annotated[Mediator, Depends(get_mediator)]
                                        ) -> list[EducationalPracticeDomainEntity]:
    group = await mediator.send(GetStudentGroupRequest(student_id=student_id))
    if not group:
        return []
    result = await mediator.send(
        educational_practices.GetEducationalPracticeListByGroupRequest(group_id=group.group_id))
    return result


@router.get("/educational_practices/pages")
async def pages(student_id: str, educational_practice_id: str, mediator: Annotated[Mediator, Depends(get_mediator)]):
    user = await mediator.send(GetUserRequest(id=student_id))
    educational_practice = await mediator.send(
        educational_practices.GetEducationalPracticeRequest(id=educational_practice_id))
    teacher_full_name = f"{educational_practice.teacher.surname} {educational_practice.teacher.name} {educational_practice.teacher.patronymic}"
    teacher_short_name = f"{educational_practice.teacher.surname} {educational_practice.teacher.name[0]}.{educational_practice.teacher.patronymic[0]}."
    student_full_name = f"{user.surname} {user.name} {user.patronymic}"
    student_short_name = f"{user.surname} {user.name[0]}.{user.patronymic[0]}."
    if not user.patronymic:
        student_short_name = f"{user.surname} {user.name[0]}."
    if not educational_practice.teacher.patronymic:
        student_short_name = f"{educational_practice.teacher.surname} {educational_practice.teacher.name[0]}."
    doc = DocxTemplate("./application/docx/educational_practice.docx")
    context = {
        "speciality": educational_practice.group.speciality,
        "group": educational_practice.group.name,
        "qualification": f"{educational_practice.group.qualification.index} {educational_practice.group.qualification.name}",
        "student_short_name": student_short_name,
        "teacher_short_name": teacher_short_name,
        "student_full_name": student_full_name,
        "teacher_full_name": teacher_full_name,
        "hours_count": educational_practice.hours_count,
        "name": educational_practice.name,
    }
    doc.render(context)
    file_name = f"{datetime.now()}.docx"
    doc.save(file_name)
    return FileResponse(path=file_name, filename="Учебная практика титульные листы.docx", media_type='multipart/form-data')


@router.get("/educational_practices/{educational_practice_id}")
async def course_work(educational_practice_id: str,
                      mediator: Annotated[Mediator, Depends(get_mediator)]) -> EducationalPracticeDomainEntity:
    response = await mediator.send(educational_practices.GetEducationalPracticeRequest(id=educational_practice_id))
    return response


@router.post("/educational_practices")
async def create(
        data: educational_practices.CreateEducationalPracticeRequest,
        mediator: Annotated[Mediator, Depends(get_mediator)]
) -> EducationalPracticeDomainEntity:
    response = await mediator.send(data)
    return response


@router.patch("/educational_practices")
async def update(
        data: educational_practices.UpdateEducationalPracticeRequest,
        mediator: Annotated[Mediator, Depends(get_mediator)]
) -> EducationalPracticeDomainEntity:
    response = await mediator.send(data)
    return response


@router.delete("/educational_practices/educational_practice_id}")
async def delete(educational_practice_id: str, mediator: Annotated[Mediator, Depends(get_mediator)]):
    response = await mediator.send(educational_practices.DeleteEducationalPracticeRequest(id=educational_practice_id))
    return response
