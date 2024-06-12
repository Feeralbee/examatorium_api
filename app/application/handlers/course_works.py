import datetime
import os
from typing import Annotated

from didiator import Mediator
from docxtpl import DocxTemplate
from fastapi import APIRouter, Depends
from loguru import logger
from starlette.responses import FileResponse

from application.dependencies import get_mediator
from domain.entities import CourseWorkDomainEntity
from domain.models.requests import course_works, GetStudentGroupRequest, GetUserRequest

router = APIRouter(tags=["course_works"])


@router.get("/course_works/all")
async def all(mediator: Annotated[Mediator, Depends(get_mediator)]) -> list[CourseWorkDomainEntity]:
    response = await mediator.send(course_works.GetCourseWorkListRequest())
    return response


@router.get("/course_works/student")
async def student_course_works(student_id: str, mediator: Annotated[Mediator, Depends(get_mediator)]
                               ) -> list[CourseWorkDomainEntity]:
    group = await mediator.send(GetStudentGroupRequest(student_id=student_id))
    if not group:
        return []
    result = await mediator.send(course_works.GetCourseWorkListByGroupRequest(group_id=group.group_id))
    return result


@router.get("/course_works/pages")
async def pages(student_id: str, course_work_id: str, mediator: Annotated[Mediator, Depends(get_mediator)]):
    user = await mediator.send(GetUserRequest(id=student_id))
    course_work = await mediator.send(course_works.GetCourseWorkRequest(id=course_work_id))
    teacher_full_name = f"{course_work.teacher.surname} {course_work.teacher.name} {course_work.teacher.patronymic}"
    teacher_short_name = f"{course_work.teacher.surname} {course_work.teacher.name[0]}.{course_work.teacher.patronymic[0]}."
    student_full_name = f"{user.surname} {user.name} {user.patronymic}"
    student_short_name = f"{user.surname} {user.name[0]}.{user.patronymic[0]}."
    if not user.patronymic:
        student_short_name = f"{user.surname} {user.name[0]}."
    if not course_work.teacher.patronymic:
        student_short_name = f"{course_work.teacher.surname} {course_work.teacher.name[0]}."
    doc = DocxTemplate("./application/docx/course_work.docx")
    context = {
        "speciality": course_work.group.speciality,
        "group": course_work.group.name,
        "qualification": f"{course_work.group.qualification.index} {course_work.group.qualification.name}",
        "discipline": f"{course_work.discipline.index} {course_work.discipline.name}",
        "student_short_name": student_short_name,
        "teacher_short_name": teacher_short_name,
        "student_full_name": student_full_name,
        "teacher_full_name": teacher_full_name
    }
    doc.render(context)
    file_name = f"{datetime.datetime.now()}.docx"
    doc.save(file_name)
    return FileResponse(path=file_name, filename="Титульные листы курсовая.docx", media_type='multipart/form-data')


@router.get("/course_works/{course_work_id}")
async def course_work(course_work_id: str,
                      mediator: Annotated[Mediator, Depends(get_mediator)]) -> CourseWorkDomainEntity:
    response = await mediator.send(course_works.GetCourseWorkRequest(id=course_work_id))
    return response


@router.post("/course_works")
async def create(
        data: course_works.CreateCourseWorkRequest,
        mediator: Annotated[Mediator, Depends(get_mediator)]
) -> CourseWorkDomainEntity:
    response = await mediator.send(data)
    return response


@router.patch("/course_works")
async def update(
        data: course_works.UpdateCourseWorkRequest,
        mediator: Annotated[Mediator, Depends(get_mediator)]
) -> CourseWorkDomainEntity:
    response = await mediator.send(data)
    return response


@router.delete("/course_works/{course_work_id}")
async def delete(course_work_id: str, mediator: Annotated[Mediator, Depends(get_mediator)]):
    response = await mediator.send(course_works.DeleteCourseWorkRequest(id=course_work_id))
    return response
