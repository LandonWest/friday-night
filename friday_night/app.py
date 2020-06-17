import logging
import os

from dotenv import load_dotenv
import falcon
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from .middleware.sqla_session_manager import SQLAlchemySessionManager
from .user_resource import UserResource
from .media_entry_resource import MediaEntryResource
from .media_item_resource import MediaItemResource


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logging.disable_existing_loggers = False


def setup_db_session(database_url):
    # Database
    engine = sqlalchemy.create_engine(database_url)
    session_factory = sessionmaker(bind=engine)

    return session_factory


def create_app(session_factory):
    # App
    api = falcon.API(middleware=[SQLAlchemySessionManager(session_factory)])

    # Resources & Routes
    user_rsc = UserResource()
    api.add_route('/api/v1/users/', user_rsc)
    api.add_route('/api/v1/users/{user_id}', user_rsc)

    media_entry_rsc = MediaEntryResource()
    api.add_route('/api/v1/users/{user_id}/media-entries/', media_entry_rsc)
    api.add_route('/api/v1/users/{user_id}/media-entries/{id}', media_entry_rsc)

    media_item_rsc = MediaItemResource()
    api.add_route('/api/v1/media-items/', media_item_rsc)
    api.add_route('/api/v1/media-items/{id}', media_item_rsc)

    return api


def get_app():
    load_dotenv()
    db_url = os.environ.get('DATABASE_URL')
    session_factory = setup_db_session(db_url)

    return create_app(session_factory)
