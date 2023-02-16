
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("follow", views.follow, name="follow"),
    path("unfollow", views.unfollow, name="unfollow"),
    path("posts/following", views.following, name='following'),

    # API Router
    path('posts', views.new_post, name='new_post'),
    path('users/<str:username>', views.index, name='user_page'),
    path('edit/<int:id>', views.edit, name="edit"),
    path('add_like/<int:id>', views.add_like, name="add_like"),
    path('remove_like/<int:id>', views.remove_like, name="remove_like")

]
