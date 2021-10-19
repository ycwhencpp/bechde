from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("listing/<int:id>", views.view_listing, name="listing"),
    path("listing/<int:id>/bid", views.place_bid, name="bid"),
    path("listing/<int:id>/comment", views.place_comment, name="comment"),
    path("listing/<int:id>/update_watchlist", views.update_watchlist, name="update_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("remove_watchlist/<int:id>", views.remove_watchlist, name="remove_watchlist"),
    path("listing/<int:id>/close_bid", views.close_bid, name="close_bid"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.view_category, name="view_category"),

]
