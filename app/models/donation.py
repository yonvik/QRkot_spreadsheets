from sqlalchemy import Integer, Column, ForeignKey, Text

from app.models.abstractclass import BaseClass


class Donation(BaseClass):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)

    def __repr__(self):
        return (
            f'user_id: {self.user_id}, '
            f'comment: {self.comment[:8]} , '
            f'{super().__repr__()}'
        )
