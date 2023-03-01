from sqlalchemy import Column, Text, Integer, ForeignKey

from app.models import InvestedBase


class Donation(InvestedBase):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)

    def __repr__(self):
        return (
            f'Пожертование №{self.id}. '
            f'Полностью потрачено: {self.fully_invested}'
        )
