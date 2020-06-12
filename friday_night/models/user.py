from sqlalchemy import Column, Integer, String
from friday_night.models import Base


class User(Base):
    """User model"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    email = Column(String(40), nullable=False, unique=True)

    def __repr__(self):
        return (
            f'<User id={self.id}, '
            f'first_name={self.first_name}, '
            f'last_name={self.last_name}, '
            f'email={self.email}>'
        )

    def __init__(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
