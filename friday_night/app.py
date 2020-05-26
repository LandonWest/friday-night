from dotenv import load_dotenv
import falcon


def create_app():
    api = falcon.API()
    return api


def get_app():
    load_dotenv
    return create_app()
