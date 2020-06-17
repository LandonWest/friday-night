import os

import falcon

from friday_night.app import logging
from friday_night.models.media_item import MediaItem


logger = logging.getLogger(__name__)


class MediaItemResource():
    """A MediaItem is the Movie/TV Series/etc. metadata info"""

    def on_get(self, req, resp, id=None):
        """Get a single Media Item or the whole Media Item collection
        GET  media-items/
        GET  media-items/<id>
        """
        if id:
            # Get Item
            media_item = self.query_item_by_id(id)
            logger.info(f'GET api/v1/media-items/{id}')
            if not media_item:
                raise falcon.HTTPNotFound(
                    title='Not found',
                    description='the requested resource was not found'
                )

            resp.media = media_item.as_dict()
        else:
            # Get Collection
            logger.info('GET api/v1/media-items/')
            resp.media = {
                'media_items': [
                    item.as_dict() for item in self.query_collection()
                ]
            }

    def on_post(self, req, resp):
        """For manually entering a Media Item's info if it's not available via OMDB API

        POST  media-items/
        """
        logger.info('POST api/v1/media-items/')
        resp.media = self.create_media_item(req.media).as_dict()

    def query_item_by_id(self, id):
        return self.session.query(MediaItem).filter_by(id=id).first()

    def query_item_by_title(self, title):
        return self.session.query(MediaItem).filter_by(title=title).first()

    def query_collection(self):
        return self.session.query(MediaItem).all()

    def create_media_item(self, media_data):
        # Check if media entry already exists.
        if self.query_item_by_title(media_data['title']):
            raise falcon.HTTPBadRequest(
                "Title exists",
                "The Media title entered already exists"
            )

        media_item = MediaItem(
            title=media_data.get('title'),
            rated=media_data.get('rated'),
            release_date=media_data.get('released'),
            runtime=media_data.get('runtime'),
            genre=media_data.get('genre'),
            director=media_data.get('director'),
            cast=media_data.get('actors'),
            plot=media_data.get('plot'),
            awards=media_data.get('awards'),
            poster=media_data.get('poster'),
            imdb_rating=media_data.get('imdb_rating'),
            rotten_tomatoes_rating=media_data.get('rotten_tomatoes_rating'),
            imdb_id=media_data.get('imdb_id'),
            media_type=media_data.get('media_type'),
            total_seasons=media_data.get('total_seasons'),
            box_office_earnings=media_data.get('box_office_earnings'),
            production_studio=media_data.get('production'),
        )

        self.session.add(media_item)
        self.session.commit()

        return media_item
