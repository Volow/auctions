from django.urls import path

from .views import *

urlpatterns = [
    path("", index, name="index"),
    path("login", login_view, name="login"),
    path("logout", logout_view, name="logout"),
    path("register", register, name="register"),
    path("lot/<int:lot_id>/detail", lot_detail, name='lot_detail_url'),
    path("lot/<int:lot_id>/detail/comment_add", comment_add, name="comment_add_url"),
    path("lot/add", lot_add, name="lot_add_url"),   
    path('catigories', catigory_list, name='catigories_list_url'),
    path('catigories/<int:catigory_id>/delete', catigory_delete, name="catigory_delete_url")
]
