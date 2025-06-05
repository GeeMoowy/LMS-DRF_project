from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import UserViewSet, PaymentViewSet, UserProfileViewSet
from users.apps import UsersConfig


app_name = UsersConfig.name

router = SimpleRouter()
router.register('users', UserViewSet, basename='users')
router.register('payments', PaymentViewSet, basename='payments')
router.register('profile', UserProfileViewSet, basename='user-profile')

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += router.urls