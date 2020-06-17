import datetime
import os

import falcon
import requests

from friday_night.app import logging
from friday_night.models.media_entry import MediaEntry
from friday_night.models.media_item import MediaItem


logger = logging.getLogger(__name__)

# OMDB_API_KEY = os.environ.get('OMDB_API_KEY') # TODO: Why can't os find the env var here but it can below in the function?
OMDB_URL = 'http://www.omdbapi.com/'


class MediaEntryResource():
    """Each Moveie/Tv Series/etc. a user wants to track will have a MediaEntry

    This will contain info including 'watched', 'watched_date', 'user_rating'
    """

    def on_get(self, req, resp, user_id, id=None):
        """Get a single Media Entry or the whole Media Entry collection
        GET  media-entries/
        GET  media-entries/<id>
        """
        if id:
            # Get Item
            media_entry = self.query_entry_by_id(id)
            logger.info(f'GET api/v1/users/{user_id}/media-entries/{id}')
            if not media_entry:
                raise falcon.HTTPNotFound(
                    title='Not found',
                    description='the requested resource was not found'
                )

            resp.media = media_entry.as_dict()
        else:
            # Get Collection
            logger.info('GET api/v1/media-entries/')
            resp.media = {
                'media_entries': [
                    entry.as_dict() for entry in self.query_collection()
                ]
            }

    def on_post(self, req, resp, user_id, id=None):
        """
        POST  media-entries/
        """
        logger.info(f'POST api/v1/users/{user_id}/media-entries/')
        resp.media = self.create_media_entry(user_id, req.media).as_dict()

    def query_entry_by_id(self, id):
        return self.session.query(MediaEntry).filter_by(id=id).first()

    def query_entry_by_title(self, title):
        return self.session.query(MediaEntry).filter_by(title=title).first()

    def query_collection(self):
        return self.session.query(MediaEntry).all()

    def fetch_media_metadata(self, title):
        payload = {'apikey': os.environ.get('OMDB_API_KEY'), 't': title}
        logger.info(f'Fetching Media metadata for "{title}" from {OMDB_URL}')
        try:
            resp = requests.get(OMDB_URL, params=payload)
            logger.info(f'{resp.status_code} | {resp.json()}')
            resp.raise_for_status()
        except requests.exceptions.HTTPError:
            logger.error(f'{OMDB_URL} returned "Unauthorized"')
            raise falcon.HTTPInternalServerError()

        if 'Error' in resp.text:
            raise falcon.HTTPNotFound(
                title='Not Found',
                description='Media title could not be found. Try a different a different title.'
            )

        return resp.json()

    def create_media_entry(self, user_id, media_data):
        title = media_data['title']
        # Check if media entry already exists.
        logger.debug(f'Checking if {title} already exists in our db...')
        if self.query_entry_by_title(title):
            raise falcon.HTTPBadRequest(
                "Title exists",
                "The Media title entered already exists"
            )

        # Check if there is already an associated Media Item for this title and create if not.
        logger.debug(f'Checking if {title} has an associated MediaItem...')
        media_item = self.session.query(MediaItem).filter_by(title=title).first()
        if not media_item:
            resp_json = self.fetch_media_metadata(title)

            try:
                release_dt = datetime.datetime.strptime(
                    resp_json.get('Released'), '%d %b %Y'
                )
                release_date = datetime.date(
                    release_dt.year, release_dt.month, release_dt.day
                )
            except ValueError as e:
                logger.error('ERROR trying to parse `release_date` from OMDB', e)
                raise falcon.HTTPInternalServerError()

            media_item = MediaItem(
                title=resp_json.get('Title'),
                rated=resp_json.get('Rated'),
                release_date=release_date,
                runtime=resp_json.get('Runtime'),
                genre=resp_json.get('Genre'),
                director=resp_json.get('Director'),
                cast=resp_json.get('Actors'),
                plot=resp_json.get('Plot'),
                awards=resp_json.get('Awards'),
                poster=resp_json.get('Poster'),
                imdb_rating=resp_json.get('imdbRating'),
                rotten_tomatoes_rating=None,  # resp_json['Ratings'][1]['Value'],  # 'Source': 'Rotten Tomatoes' TODO: THIS IS BRITTLE!
                imdb_id=resp_json.get('imdbID'),
                media_type=resp_json.get('Type'),
                total_seasons=resp_json.get('totalSeasons'),
                box_office_earnings=resp_json.get('BoxOffice'),
                production_studio=resp_json.get('Production'),
            )
            try:
                self.session.add(media_item)
                self.session.commit()
            except Exception as e:
                logger.error(e)
                raise falcon.HTTPInternalServerError(
                    title='Database Error',
                    description='There was a problem saving the data'
                )

        media_item_id = self.session.query(MediaItem.id).filter_by(title=title)
        req_watched_date = media_data.get('watched_date')
        if req_watched_date:
            try:
                watched_dt = datetime.datetime.strptime(req_watched_date, '%Y-%m-%d')
                watched_date = datetime.date(
                    watched_dt.year, watched_dt.month, watched_dt.day
                )
            except ValueError as e:
                logger.error('ERROR trying to parse `watched_date` from user input', e)
                raise falcon.HTTPInternalServerError()
        else:
            watched_date = None

        data = dict(
            title=media_data.get('title'),
            user_id=user_id,
            media_item_id=media_item_id
        )
        if watched_date:
            data.update({
                'watched': True,
                'watched_date': watched_date,
            })

        media_entry = MediaEntry(**data)

        try:
            self.session.add(media_entry)
            self.session.commit()
        except Exception as e:
            logger.error(e)
            raise falcon.HTTPInternalServerError(
                title='Database Error',
                description='There was a problem saving the data'
            )

        return media_entry
