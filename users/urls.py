from rest_framework.routers import SimpleRouter

from users.views import UserViewSet, PaymentViewSet, UserProfileViewSet
from users.apps import UsersConfig


app_name = UsersConfig.name

router = SimpleRouter()
router.register('users', UserViewSet, basename='users')
router.register('payments', PaymentViewSet, basename='payments')
router.register('profile', UserProfileViewSet, basename='user-profile')

urlpatterns = []

urlpatterns += router.urls