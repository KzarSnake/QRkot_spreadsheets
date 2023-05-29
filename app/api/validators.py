from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject


async def is_name_duplicate(name: str, session: AsyncSession) -> None:
    duplicate = await charity_project_crud.get_obj_by_name(name, session)
    if duplicate:
        raise HTTPException(
            HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def is_project_exist(
    project_id: int, session: AsyncSession
) -> Optional[CharityProject]:
    project = await charity_project_crud.get(project_id, session)
    if not project:
        raise HTTPException(
            HTTPStatus.NOT_FOUND, detail='Проект не существует!'
        )
    return project


async def is_project_invested_on_edit(
    project: CharityProject,
    new_full_amount: Optional[int] = None,
) -> None:
    if project.fully_invested:
        raise HTTPException(
            HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!',
        )
    if new_full_amount is None:
        return project
    if new_full_amount < project.invested_amount:
        raise HTTPException(
            HTTPStatus.BAD_REQUEST,
            detail='Общяя стоимость проекта не может быть изменена в меньшую сторону!',
        )


async def is_project_invested_on_delete(project: CharityProject) -> None:
    if project.fully_invested:
        raise HTTPException(
            HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!',
        )
    if project.invested_amount > 0:
        raise HTTPException(
            HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!',
        )
