from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_charity_project_name_duplicate(
        charity_project_name: str,
        session: AsyncSession,
) -> None:
    charity_project_id = await charity_project_crud.get_project_id_by_name(
        charity_project_name=charity_project_name,
        session=session
    )
    if charity_project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_charity_project_exist(
        charity_project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get_by_id(
        charity_project_id=charity_project_id,
        session=session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )
    return charity_project


async def check_project_invest_amount_is_empty(
        charity_project_obj: CharityProject,
):
    project_invested_amount = charity_project_obj.invested_amount
    if project_invested_amount != 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(
                'В проект были внесены средства, '
                'не подлежит удалению!'
            )
        )


async def check_project_is_close(
        charity_project_obj: CharityProject,
):
    if charity_project_obj.close_date is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(
                'Закрытый проект нельзя редактировать!'
            )
        )


async def check_full_amount_no_less_than_invested_amount(
        invested_amount: int,
        new_full_amount: int,
) -> None:
    if new_full_amount < invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=(
                'Новая требуемая сумма должна быть не меньше старой!'
            )
        )
