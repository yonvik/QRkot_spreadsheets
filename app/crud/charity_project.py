from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import BaseCRUD
from app.models.charity_project import CharityProject


class CharityProjectCRUD(BaseCRUD):
    """Дополнение базовой реализации CRUD для модели."""

    async def get_charity_project_by_id(
        self,
        project_name: str,
        session: AsyncSession
    ) -> Optional[int]:
        project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        return project_id.scalars().first()

    async def remove(
        self,
        db_obj,
        session: AsyncSession
    ) -> CharityProject:
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def update(
        self,
        obj_in,
        db_obj,
        session: AsyncSession,
        commit: bool = True
    ) -> CharityProject:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        if commit:
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession
    ) -> Optional[list[dict[str, str]]]:
        available_projects = await session.execute(
            select(CharityProject).where(CharityProject.fully_invested)
        )
        list_projects = available_projects.scalars().all()
        return list_projects


charityproject_crud = CharityProjectCRUD(CharityProject)
