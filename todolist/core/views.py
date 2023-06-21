from rest_framework.generics import CreateAPIView

from .models import User
from .serializers import UserCreateSerializer


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
