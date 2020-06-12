import logging
import os

from dotenv import load_dotenv
import falcon
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from .middleware.sqla_session_manager import SQLAlchemySessionManager
from .users import User


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
    user_resource = User()
    api.add_route('/api/v1/users', user_resource)
    api.add_route('/api/v1/users/{user_id}', user_resource)

    return api


def get_app():
    load_dotenv()
    db_url = os.environ.get('DATABASE_URL')
    session_factory = setup_db_session(db_url)

    return create_app(session_factory)
