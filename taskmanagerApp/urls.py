from django.urls import path
from . import views

urlpatterns = [
    # /taskmanagerApp/login/
    path("login", views.login, name="login"),
    # /taskmanagerApp/register/
    path("register", views.register, name="register"),
    # /taskmanagerApp/register/conf
    path("register/conf", views.register_conf, name="register_conf"),
    # /taskmanagerApp/
    path("", views.top, name="top"),
    # /taskmanagerApp/confirm/
    path("confirm", views.confirm_today_task, name="confirm_today_task"),
    # /taskmanagerApp/my-page/
    path("my-page", views.my_page, name="my-page"),
    # /taskmanagerApp/logout/
    path("logout", views.logout, name="logout")
]