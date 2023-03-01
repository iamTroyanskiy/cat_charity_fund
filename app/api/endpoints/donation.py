from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationDB, DonationCreate, DonationDBUser
from app.services.investment import run_investment_process

router = APIRouter()


@router.post(
    '/',
    response_model=DonationDBUser,
    response_model_exclude_none=True,
)
async def create_new_donation(
        donation: DonationCreate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
):
    """Сделать пожертвование"""
    new_donation = await donation_crud.create(
        obj_in=donation,
        user=user,
        session=session,
    )
    new_donation = await run_investment_process(
        obj_in=new_donation,
        session=session
    )
    return new_donation


@router.get(
    '/',
    response_model=List[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров. <br />
    Возвращает список всех пожертвований.
    """
    all_donations = await donation_crud.get_multi(
        session=session
    )
    return all_donations


@router.get(
    '/my',
    response_model_exclude_none=True,
    response_model=List[DonationDBUser]
)
async def get_user_donations(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
):
    """Вернуть список пожертвований пользователя, выполняющего запрос."""
    user_donations = await donation_crud.get_by_user(
        user=user,
        session=session
    )
    return user_donations
