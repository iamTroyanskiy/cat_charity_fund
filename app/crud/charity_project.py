from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):

    async def update(
            self,
            charity_project_obj,
            charity_project_in,
            session: AsyncSession,
    ):
        update_data = charity_project_in.dict(exclude_unset=True)
        for field in update_data:
            setattr(charity_project_obj, field, update_data[field])
        session.add(charity_project_obj)
        await session.commit()
        await session.refresh(charity_project_obj)
        return charity_project_obj

    async def remove(
            self,
            charity_project_obj,
            session: AsyncSession
    ):
        await session.delete(charity_project_obj)
        await session.commit()
        return charity_project_obj

    async def get_by_id(
            self,
            charity_project_id: int,
            session: AsyncSession,
    ):
        charity_project_obj = await session.execute(
            select(self.model).where(
                self.model.id == charity_project_id
            )
        )
        charity_project_obj = charity_project_obj.scalars().first()
        return charity_project_obj

    async def get_project_id_by_name(
            self,
            charity_project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        charity_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == charity_project_name
            )
        )
        charity_project_id = charity_project_id.scalars().first()
        return charity_project_id


charity_project_crud = CRUDCharityProject(CharityProject)
