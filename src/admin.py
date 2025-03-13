from src import db, app
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_login import current_user, logout_user
from src.models import UserRole
from flask import redirect

class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and \
            (current_user.userRole == UserRole.ADMIN or current_user.userRole == UserRole.TEACHER)

class MyAdminIndex(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')

class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated

class Register(BaseView):
    @expose('/')
    def __index__(self):

        return redirect('/register')

    def is_accessible(self):
        return current_user.is_authenticated and \
            (current_user.userRole == UserRole.ADMIN or current_user.userRole == UserRole.TEACHER)

admin = Admin(app=app, name='QUẢN TRỊ ĐIỂM DANH SINH VIÊN', template_mode='bootstrap4', index_view=MyAdminIndex())
admin.add_view(Register(name='Đăng ký'))
admin.add_view(LogoutView(name='Đăng xuất'))