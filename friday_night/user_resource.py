import falcon

from friday_night.app import logging
from friday_night.models.user import User as User

logger = logging.getLogger(__name__)


class UserResource(object):
    """Contains HTTP responders for User resource"""

    # GET users/
    # GET users/usr_123

    def get_user_by_id(self, id):
        return self.session.query(User).filter_by(id=id).first()

    def get_user_by_email(self, email):
        return self.session.query(User).filter_by(email=email).first()

    def on_get(self, req, resp, user_id=None):
        # TODO: this is probably where we need a query string - ex. users/q? id=1 or email=test@example.com
        def get_user_item(user_id):
            """Handles GET requests. (GET: /users/{identifier})"""
            logger.info(f'GET /users/{user_id}')
            user = self.get_user_by_id(user_id)
            if not user:
                raise falcon.HTTPNotFound(
                    title='Not found',
                    description='the requested resource was not found'
                )

            resp.media = user.as_dict()

        def get_user_collection():
            logger.info('GET /users')
            users_list = self.session.query(User).all()
            resp.media = {'users': [user.as_dict() for user in users_list]}

        if user_id:
            get_user_item(user_id)
        else:
            get_user_collection()

    def on_post(self, req, resp, user_id=None):
        """Handles POST requests. (POST: /users)"""

        # TODO: need to check email isn't aleady in the db
        # sqlalchemy.exc.IntegrityError: (sqlite3.IntegrityError) UNIQUE constraint failed: users.email
        logger.info('POST /users')

        email = req.media['email']
        if self.get_user_by_email(email):
            raise falcon.HTTPBadRequest(
                "Email in use",
                "The email entered is already in use. Please use a different email"
            )

        try:
            new_user = User(
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
            resp.media = new_user.as_dict()
