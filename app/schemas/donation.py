from datetime import datetime
from typing import Optional

from pydantic import PositiveInt, NonNegativeInt, Field

from app.schemas.base import BaseSchema


class DonationBase(BaseSchema):
    full_amount: PositiveInt
    comment: Optional[str]


class DonationCreate(DonationBase):
    pass


class DonationDBUser(DonationBase):
    id: int
    create_date: datetime


class DonationDB(DonationDBUser):
    user_id: int
    invested_amount: NonNegativeInt
    fully_invested: bool
    close_date: Optional[datetime]
