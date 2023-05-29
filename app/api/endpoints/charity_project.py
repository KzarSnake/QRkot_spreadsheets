from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    is_name_duplicate,
    is_project_exist,
    is_project_invested_on_delete,
    is_project_invested_on_edit,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject
from app.models.donation import Donation
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.servises.investment import check_uninvested_amounts

router = APIRouter()


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude={'close_date'},
)
async def get_all_projects(
    session: AsyncSession = Depends(get_async_session),
) -> List[CharityProject]:
    return await charity_project_crud.get_all(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=(Depends(current_superuser),),
)
async def create_charity_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProject:
    await is_name_duplicate(project.name, session)
    new_project = await charity_project_crud.create(project, session)
    return await check_uninvested_amounts(Donation, new_project, session)


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=(Depends(current_superuser),),
)
async def remove_charity_project(
    project_id: int, session: AsyncSession = Depends(get_async_session)
) -> CharityProject:
    project = await is_project_exist(project_id, session)
    await is_project_invested_on_delete(project)
    return await charity_project_crud.remove(project, session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=(Depends(current_superuser),),
)
async def update_charity_project(
    project_id: int,
    updated_project: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProject:
    project = await is_project_exist(project_id, session)
    await is_project_invested_on_edit(
        project,
        new_full_amount=updated_project.full_amount,
    )
    if updated_project.name is not None:
        await is_name_duplicate(updated_project.name, session)
    project = await charity_project_crud.update(
        project, updated_project, session
    )
    if updated_project.full_amount is not None:
        return await check_uninvested_amounts(Donation, project, session)
    return project
