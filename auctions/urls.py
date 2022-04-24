from unicodedata import name
from django.urls import path

from .views import *

urlpatterns = [
    path("", index, name="index"),
    path("login", login_view, name="login"),
    path("logout", logout_view, name="logout"),
    path("register", register, name="register"),
    path("add/lot", add_lot, name="add_lot"),   
    path('catigories', catigory_list, name='catigories_list_url'),
    path('catigories/<int:catigory_id>/delete', catigory_delete, name="catigory_delete_url")
]
