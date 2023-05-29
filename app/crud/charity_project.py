from datetime import timedelta
from typing import Dict, List, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):
    async def get_obj_by_name(
        self, name: str, session: AsyncSession
    ) -> CharityProject:
        db_obj = await session.execute(
            select(CharityProject).where(CharityProject.name == name)
        )
        return db_obj.scalars().first()

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession,
    ) -> List[Dict[str, Union[str, timedelta]]]:
        projects = await session.execute(
            select(
                [
                    CharityProject.name,
                    CharityProject.fundraising_time,
                    CharityProject.description,
                ]
            )
            .where(CharityProject.fully_invested.is_(True))
            .order_by(CharityProject.fundraising_time)
        )
        return projects.all()


charity_project_crud = CRUDCharityProject(CharityProject)
