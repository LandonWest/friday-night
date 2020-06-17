from sqlalchemy import (
    Column,
    Date,
    Float,
    Integer,
    String,
    Text
)

from friday_night.models import Base


class MediaItem(Base):

    __tablename__ = 'media_items'

    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False, unique=True)
    rated = Column(String(8))
    release_date = Column(Date)
    runtime = Column(String(8))
    genre = Column(String(80))
    director = Column(String(20))
    cast = Column(String(120))
    plot = Column(Text)
    awards = Column(String(120))
    poster = Column(String(180))
    imdb_rating = Column(Float)
    rotten_tomatoes_rating = Column(String(20))
    imdb_id = Column(String(20))
    media_type = Column(String(20))
    total_seasons = Column(Integer)
    box_office_earnings = Column(Integer)
    production_studio = Column(String(40))

    def __repr__(self):
        return '<MediaItem(id={}, title="{}", media_type="{}", genre="{}", rated="{}")>'.format(
                self.id, self.title, self.media_type, self.genre, self.rated
        )

    def as_dict(self):
        """Converts the User model into a Dict that can be returned as json in a response"""
        # return {c.name: getattr(self, c.name) for c in self.__table__.columns}
        # TODO: NEED A SERIALIZER SO I DON"T HAVE TO CONVERT PYTHON DATE OBJECTS TO STRINGS FOR JSON AND VICE VERSA!
        return {
            'id': self.id,
            'title': self.title,
            'rated': self.rated,
            'release_date': str(self.release_date),  # BOO! Don't Do This! Use Marshmallow or something!
            'runtime': self.runtime,
            'genre': self.genre,
            'director': self.director,
            'cast': self.cast,
            'plot': self.plot,
            'awards': self.awards,
            'poster': self.poster,
            'imdb_rating': self.imdb_rating,
            'rotten_tomatoes_rating': self.rotten_tomatoes_rating,
            'imdb_id': self.imdb_id,
            'media_type': self.media_type,
            'total_seasons': self.total_seasons,
            'box_office_earnings': self.box_office_earnings,
            'production_studio': self.production_studio,
        }
