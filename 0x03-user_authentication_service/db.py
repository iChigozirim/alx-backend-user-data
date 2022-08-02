"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import NoResultFound

from user import Base
from user import User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email, hashed_pwd):
        """Saves a user to the database."""
        user = User(email=email, hashed_password=hashed_pwd)
        self._session.add(user)
        self._session.commit()

        return user

    def find_user_by(self, **kwargs):
        """Returns the first row found in the users table as filtered by the
        input arguments.
        """
        user = self._session.query(User).filter_by(**kwargs).first()
        if user is None:
            raise NoResultFound

        return user

    def update_user(self, user_id, **kwargs):
        """Updates a User instance."""
        user = self.find_user_by(id=user_id)
        for k, v in kwargs.items():
            if k != 'id' and type(v) != str:
                raise ValueError
            setattr(user, k, v)

        return None