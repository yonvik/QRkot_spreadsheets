from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud import charity_project
from app.services.google_api import (
    set_user_permissions, spreadsheets_create, spreadsheets_update_value
)

router = APIRouter()


@router.post(
    '/',
    response_model=list[dict[str, int]],
    dependencies=[Depends(current_superuser)],
)
async def get_report(
        session: AsyncSession = Depends(get_async_session),
        wrapper_services: Aiogoogle = Depends(get_service)

):
    """Только для суперюзеров."""
    projects = await charity_project.get_projects(
        session
    )
    spreadsheet_id = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheet_id, wrapper_services)
    try:
        await spreadsheets_update_value(
            spreadsheet_id,
            projects,
            wrapper_services
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    return projects
