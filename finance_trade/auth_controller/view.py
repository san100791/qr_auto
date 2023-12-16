import logging

from flask import Blueprint, views, request, Response
from finance_trade.services.user_service import UserService
from finance_trade.auth_controller.shemes.request_schemes import CreateUserRequestSchema
from finance_trade.auth_controller.shemes.response_schemes import UserResponseSchema


logger = logging.getLogger(__name__)

user_bp = Blueprint("user_bp", __name__)


class CreateUserView(views.MethodView):
    def post(self, request):
        user_data = CreateUserRequestSchema().load(request.get_json())
        s = UserService()
        user, user_session = s.create_user(
            name=user_data.name,
            surname=user_data.surname,
            password=user_data.password,
            email=user_data.email,
            phone=user_data.phone,
        )
        r = Response(data=UserResponseSchema().dump(user))
        r.set_cookie("sid", user_session.cookie, expires=user_session.expired_at, samesite=True, secure=True, httponly=True, lax=True, domain="localhost")
        r.status_code = 201
        return r
    

user_bp.add_url_rule("/signup", view_func=CreateUserView.as_view("create_user"))