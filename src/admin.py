from src import db, app, admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose, AdminIndexView
from flask_login import current_user, logout_user
from src.models import User, UserRole
from flask import redirect

class AuthenticatedBaseView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated

class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == UserRole.ADMIN

class LogoutView(AuthenticatedBaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

class Register(AuthenticatedBaseView):
    @expose('/')
    def __index__(self):

        return redirect('/register')


admin.add_view(AuthenticatedModelView(User, db.session, name='Người dùng'))
admin.add_view(Register(name='Đăng ký'))
admin.add_view(LogoutView(name='Đăng xuất'))
