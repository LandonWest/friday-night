import falcon

from friday_night.app import logging
from friday_night.models.user import User as UserModel

logger = logging.getLogger(__name__)


class User(object):
    """Contains HTTP responders for User resource"""

    def on_get(self, req, resp, user_id=None):

        def fetch_user_by_id(user_id):
            """Handles GET requests. (GET: /users/{identifier})"""
            logger.info(f'GET /users/{user_id}')
            user = self.session.query(UserModel).filter_by(id=user_id).first()
            if not user:
                raise falcon.HTTPNotFound(
                    title='Not found',
                    description='the requested resource was not found'
                )

            resp.media = {'user': user.as_dict()}

        def fetch_users():
            logger.info('GET /users')
            users_list = self.session.query(UserModel).all()
            resp.media = {'users': [user.as_dict() for user in users_list]}

        if user_id:
            fetch_user_by_id(user_id)
        else:
            fetch_users()

    def on_post(self, req, resp):
        """Handles POST requests. (POST: /users)"""

        # TODO: need to check email isn't aleady in the db
        # sqlalchemy.exc.IntegrityError: (sqlite3.IntegrityError) UNIQUE constraint failed: users.email
        logger.info('POST /users')
        try:
            new_user = UserModel(
                first_name=req.media['first_name'],
                last_name=req.media['last_name'],
                email=req.media['email'],
            )
        except (TypeError, KeyError) as e:
            split_str = str(e).split(':')
            missing_params = split_str[1] if len(split_str) > 1 else split_str[0]
            missing_params = missing_params.strip().replace("'", "")

            raise falcon.HTTPMissingParam(missing_params)

        if new_user:
            self.session.add(new_user)
            self.session.commit()
            resp.status = falcon.HTTP_CREATED
            resp.media = {'user': new_user.as_dict()}
