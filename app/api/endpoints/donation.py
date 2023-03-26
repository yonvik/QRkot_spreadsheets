from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import CharityProject, User
from app.schemas.donation import DonationCreate, ExtendedDonationtDB, DonationtDB
from app.services.investment import investment_process

router = APIRouter()


@router.get(
    '/',
    response_model=List[ExtendedDonationtDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    """Получение списка всех пожертвований - только для суперюзеров."""
    return await donation_crud.get_multi(session=session)


@router.get(
    '/my',
    response_model=List[DonationtDB],
    response_model_exclude_none=True
)
async def get_user_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Получение списка всех пожертвований текущего пользователя."""
    return await donation_crud.get_user_donations(user, session)


@router.post(
    '/',
    response_model=DonationtDB,
    response_model_exclude_none=True
)
async def create_donation(
    donation: DonationCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Создание пожертвования - для аутентифицированного пользователя."""
    donation = await donation_crud.create(
        donation,
        session,
        user,
        commit=False
    )
    model_objects = await donation_crud.get_investment_active(
        session, CharityProject
    )
    if model_objects:
        session.add_all(investment_process(donation, model_objects))
    await session.commit()
    await session.refresh(donation)
    return donation
