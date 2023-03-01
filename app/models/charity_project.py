from sqlalchemy import Column, String, Text

from app.models import InvestedBase


class CharityProject(InvestedBase):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return (
            f'Проект {self.name}. '
            f'Требует пожертвований: {self.fully_invested}'
        )