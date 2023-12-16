import datetime
from finance_trade.exceptions import UserAlreadyExists
from finance_trade.services.core import DatabaseServiceMixin
from finance_trade.models import User, UserSerssion
from finance_trade.utils import random_string
import hashlib


class UserService(DatabaseServiceMixin):

    def __make_cookie_object(self, user):
        cookie = hashlib.sha512(random_string.encode()).hexdigest()
        expire_at = datetime.now() + datetime.timedelta(days=30)
        user_session = UserSerssion(user_id=user.id, cookie=cookie, expired_at=expire_at)
        return user_session

    def get_user(self, user_id: int):
        return self.db_session.query(User).filter(User.id == user_id).first()
    
    def get_user_by_email(self, email: str):
        return self.db_session.query(User).filter(User.email == email).first()
    
    def create_user(self, name, surname, password, email, phone):
        user = self.get_user_by_email(email)
        if user:
            raise UserAlreadyExists(f"User with provided email {email} already exists")
        paswd = hashlib.sha512(password.encode()).hexdigest()
        user = User(name=name, surname=surname, password=paswd, email=email, phone=phone)
        user_session = self.__make_cookie_object(user)
        self.db_session.add(user)
        self.db_session.add(user_session)
        self.db_session.commit()
        return user, user_session
    
    def login(self, email, password):
        paswd = hashlib.sha512(password.encode()).hexdigest()
        user = self.db_session.query(User).filter(User.email == email, User.password == paswd).first()
        if user:
            user_session = self.__make_cookie_object(user)
            self.db_session.add(user_session)
            self.db_session.commit()
        else:
            user = None
            user_session = None
        return user, user_session