from django.urls import path
from . import views

urlpatterns = [
    # /taskmanager/
    path("", views.index, name="index"),
]