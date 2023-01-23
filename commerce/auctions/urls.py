from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('new', views.create_listing, name='new'),
    path('list_filter', views.list_filter, name='list_filter'),
    path('listing/<int:id>', views.listing, name='listing'),
    path('removeWatchlistOnListingPage/<int:id>', views.remove_watchlist_on_listing_page, name='removeWatchlistOnListingPage'),
    path('removeEntryInWatchlist/<int:id>', views.remove_entry_in_watchlist, name='removeEntryInWatchlist'),
    path('addWatchlist/<int:id>', views.add_watchlist, name='addWatchlist'),
    path('watchlist', views.view_watchlist, name='watchlist'),
    path('add_comment/<int:id>', views.add_comment, name='add_comment'),
    path('make_bid/<int:id>', views.make_bid, name='make_bid'),
    path('close_listing/<int:id>', views.close_listing, name='close_listing'),
    path('brands', views.brands, name='brands'),
    path('brands/<int:id>', views.brand_entries, name='brand_entries'),
    path('users/<int:id>', views.users, name='users'),
    path('users/<int:id>/entries', views.user_entries, name='user_entries'),
]

