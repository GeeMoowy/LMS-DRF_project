from django.urls import path

from users.views import UserProfileUpdateApiView
from users.apps import UsersConfig


app_name = UsersConfig.name

urlpatterns = [
    path('profile/update/<int:pk>/', UserProfileUpdateApiView.as_view(), name='profile_update'),
]