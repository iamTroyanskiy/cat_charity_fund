from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import CharityProject, Donation


def close_obj(
        current_obj,
        list_objs: list,
) -> None:
    current_obj.invested_amount = current_obj.full_amount
    current_obj.fully_invested = True
    current_obj.close_date = datetime.utcnow()
    list_objs.pop(0)


async def run_investment_process(
        obj_in,
        session: AsyncSession,
):
    no_fully_projects = await (
        charity_project_crud.is_no_full_invested_objs_exist(
            session=session
        )
    )
    no_fully_donations = await (
        donation_crud.is_no_full_invested_objs_exist(
            session=session
        )
    )
    while len(no_fully_projects) != 0 and len(no_fully_donations) != 0:
        project: CharityProject = no_fully_projects[0]
        donation: Donation = no_fully_donations[0]
        project_left_to_full = (
            project.full_amount - project.invested_amount
        )
        donation_left_to_full = (
            donation.full_amount - donation.invested_amount
        )
        if project_left_to_full > donation_left_to_full:
            project.invested_amount += donation_left_to_full
            close_obj(
                current_obj=donation,
                list_objs=no_fully_donations
            )
        else:
            close_obj(
                current_obj=project,
                list_objs=no_fully_projects
            )
            if project_left_to_full == donation_left_to_full:
                close_obj(
                    current_obj=donation,
                    list_objs=no_fully_donations
                )
            else:
                donation.invested_amount += project_left_to_full
        session.add(project)
        session.add(donation)
    await session.commit()
    await session.refresh(obj_in)
    return obj_in
