from django.urls import path
from . import views

urlpatterns = [
    # /taskmanagerApp/
    path("", views.top, name="top"),
]