from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class CRUDBase:

    def __init__(self, model):
        self.model = model

    async def get_multi(
            self,
            session: AsyncSession,
    ):
        all_db_obj = await session.execute(
            select(self.model)
        )
        all_db_obj = all_db_obj.scalars().all()
        return all_db_obj

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            user: Optional[User] = None,
    ):
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def is_no_full_invested_objs_exist(
            self,
            session: AsyncSession
    ):
        no_full_invested_objs = await session.execute(
            select(self.model).where(
                self.model.fully_invested == False # noqa
            ).order_by(
                self.model.create_date
            )
        )
        no_full_invested_objs = no_full_invested_objs.scalars().all()
        return no_full_invested_objs
