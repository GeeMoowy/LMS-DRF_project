from rest_framework.exceptions import NotFound
from rest_framework.generics import UpdateAPIView

from users.models import User
from users.serializers import UserProfileSerializer


class UserProfileUpdateApiView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
