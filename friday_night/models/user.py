from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from friday_night.models import Base


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    email = Column(String(40), nullable=False, unique=True)
    media_entries = relationship('MediaEntry')

    def __repr__(self):
        return (
            f'<User(id={self.id}, '
            f'first_name="{self.first_name}", '
            f'last_name="{self.last_name}", '
            f'email="{self.email}")>'
        )

    def as_dict(self):
        """Converts the User model into a Dict that can be returned as json in a response"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
