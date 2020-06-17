from sqlalchemy import Boolean, Column, Date, Float, ForeignKey, Integer, String

from friday_night.models import Base


class MediaEntry(Base):

    __tablename__ = 'media_entries'

    id = Column(Integer, primary_key=True)
    title = Column(String(40), nullable=False)
    watched = Column(Boolean, default=False)
    watched_date = Column(Date)  # datetime.date()
    user_rating = Column(Float)  # 6.5 (out of 10)

    user_id = Column(Integer, ForeignKey('users.id'))
    media_item_id = Column(Integer, ForeignKey('media_items.id'))

    def __repr__(self):
        return '<MediaEntry(id={}, watched={}, watched_date={}, user_rating={})>'.format(
            self.id, self.watched, self.watched_date, self.user_rating
        )

    def as_dict(self):
        """Converts the User model into a Dict that can be returned as json in a response"""
        # return {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return {
            'id': self.id,
            'title': self.title,
            'watched': self.watched,
            'watched_date': str(self.watched_date), # TODO: Reeeeally need to use a data serializer like Marshmallow...
            'user_rating': self.user_rating,
            'user_id': self.user_id,
            'media_item_id': self.media_item_id
        }
