import datetime
from finance_trade.exceptions import NotAuthorized
from finance_trade.services.core import DatabaseServiceMixin
from finance_trade.models import UserSerssion

class AuthService(DatabaseServiceMixin):
    def auth(self, request):
        cookie = request.cookies.get("sid")
        user_session = self.db_session.query(UserSerssion).filter(UserSerssion.cookie == cookie).first()
        if not user_session and user_session.expired_at < datetime.now():
            raise NotAuthorized("User not auth")
        return user_session.user_id