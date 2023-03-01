from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charity_project_name_duplicate,
    check_charity_project_exist,
    check_project_invest_amount_is_empty,
    check_project_is_close,
    check_full_amount_no_less_than_invested_amount,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB, CharityProjectUpdate
)
from app.services.investment import run_investment_process

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров. <br />
    Создаёт благотворительный проект.
    """
    await check_charity_project_name_duplicate(
        charity_project_name=charity_project.name,
        session=session
    )
    new_charity_project = await charity_project_crud.create(
        obj_in=charity_project,
        session=session,
    )
    new_charity_project = await run_investment_process(
        obj_in=new_charity_project,
        session=session
    )
    return new_charity_project


@router.get(
    '/',
    response_model_exclude_none=True,
    response_model=List[CharityProjectDB]
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
):
    """Возвращает список всех проектов."""
    all_charity_projects = await charity_project_crud.get_multi(
        session=session
    )
    return all_charity_projects


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров. <br />
    Закрытый проект нельзя редактировать;
    нельзя установить требуемую сумму меньше уже вложенной.
    """
    charity_project = await check_charity_project_exist(
        charity_project_id=project_id,
        session=session
    )
    await check_project_is_close(
        charity_project_obj=charity_project,
    )
    if obj_in.name is not None:
        await check_charity_project_name_duplicate(
            charity_project_name=obj_in.name,
            session=session
        )
    if obj_in.full_amount is not None:
        await check_full_amount_no_less_than_invested_amount(
            invested_amount=charity_project.invested_amount,
            new_full_amount=obj_in.full_amount,
        )
    charity_project = await charity_project_crud.update(
        charity_project_obj=charity_project,
        charity_project_in=obj_in,
        session=session,
    )
    return charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров. <br />
    Удаляет проект. Нельзя удалить проект, в который уже были инвестированы
    средства, его можно только закрыть.
    """
    charity_project = await check_charity_project_exist(
        charity_project_id=project_id,
        session=session
    )
    await check_project_invest_amount_is_empty(
        charity_project_obj=charity_project,
    )
    await check_project_is_close(
        charity_project_obj=charity_project,
    )
    charity_project = await charity_project_crud.remove(
        charity_project_obj=charity_project,
        session=session
    )
    return charity_project
