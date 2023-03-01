from datetime import datetime
from typing import Optional

from pydantic import (
    Field,
    PositiveInt,
    NonNegativeInt,
    validator,
)

from app.schemas.base import BaseSchema


class CharityProjectBase(BaseSchema):
    name: Optional[str] = Field(
        None,
        max_length=100,
    )
    description: Optional[str]
    full_amount: Optional[PositiveInt]


class CharityProjectUpdate(CharityProjectBase):

    @validator('*')
    def fields_cannot_be_null(cls, value):
        if not value:
            raise ValueError(f'Поля в запросе не могут быть пустыми!')
        return value


class CharityProjectCreate(CharityProjectUpdate):
    name: str = Field(
        ...,
        max_length=100,
    )
    description: str
    full_amount: PositiveInt


class CharityProjectDB(CharityProjectBase):
    id: int
    name: str = Field(
        ...,
        max_length=100,
    )
    description: str
    full_amount: PositiveInt
    invested_amount: NonNegativeInt
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]
