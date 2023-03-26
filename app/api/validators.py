from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charityproject_crud
from app.models import CharityProject

PROJECT_NAME_ALREDY_EXISTS = 'Проект с таким именем уже существует!'
PROJECT_NOT_FOUND = 'Не найден благотворительный проект по id: {project_id}'
CLOSED_PROJECT = 'Закрытый проект нельзя редактировать!'
CANNOT_REMOVED_WITH_FINDS = 'В проект были внесены средства, не подлежит удалению!'
AMOUNT_LESS = 'Нельзя установить сумму меньше уже вложенной: {invested}'


async def check_project_name(
    project_name: str,
    session: AsyncSession
) -> None:
    """Вызывает исключение, если проект с таким именем уже существует."""

    project = await charityproject_crud.get_charity_project_by_id(
        project_name, session
    )
    if project:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=PROJECT_NAME_ALREDY_EXISTS
        )


async def check_existence(
    project_id: int,
    session: AsyncSession
) -> CharityProject:
    """Вызывает исключение, если в базе данных не найден проект с таким именем."""

    project = await charityproject_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=PROJECT_NOT_FOUND.format(project_id=project_id)
        )
    return project


def check_amount(obj, new_amount=None):
    """
    Вызывает исключение, если в проект уже были инвестированы средства
    меньше предыдущей или если сумма пожертвований неположительна.
    """

    invested = obj.invested_amount
    if new_amount:
        if invested > new_amount:
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail=AMOUNT_LESS.format(invested=invested)
            )
    elif invested > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=CANNOT_REMOVED_WITH_FINDS
        )
    return obj


def check_closed(obj):
    """Вызывает исключение, если проект уже закрыт"""

    if obj.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=CLOSED_PROJECT
        )
