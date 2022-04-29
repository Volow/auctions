from django.urls import path

from .views import *

urlpatterns = [
    path("", index, name="index"),
    path("login", login_view, name="login"),
    path("logout", logout_view, name="logout"),
    path("register", register, name="register"),
    path("lot/<int:lot_id>/detail", lot_detail, name='lot_detail_url'),
    path("lot/<int:lot_id>/detail/comment_add", comment_add, name="comment_add_url"),
    path("lot/<int:lot_id>/detail/bid_add", bid_add, name="bid_add_url"),
    path("lot/add", lot_add, name="lot_add_url"), 
    path("lot/<int:lot_id>/close", lot_close, name="lot_close_url"),
    path("lot/<int:lot_id>/watchlist/add", add_to_watchlist, name="add_to_watchlist_url"),
    path('watchlist', watchlist, name="watchlist"),
    path('watchlist/<int:lot_id>/delete', watchlist_lot_delete, name="watchlist_lot_delete_url"),
    path('catigories', catigory_list, name='catigories_list_url'),
    path('catigories/<int:catigory_id>/delete', catigory_delete, name="catigory_delete_url")
]
