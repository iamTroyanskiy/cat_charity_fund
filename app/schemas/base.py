from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt


class BaseSchema(BaseModel):

    class Config:
        extra = Extra.forbid
        orm_mode = True
