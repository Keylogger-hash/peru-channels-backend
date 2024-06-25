from rest_framework import generics
from rest_framework import mixins
from django.contrib.auth.models import User
from .serializers import UserSerializer, UserRegisterSerializer
from rest_framework.permissions import IsAuthenticated
# Create your views here.


class UserList(
    mixins.ListModelMixin, generics.GenericAPIView
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class UserRegister(
    generics.GenericAPIView, mixins.CreateModelMixin
):
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UserDetail(
    mixins.RetrieveModelMixin,
    generics.GenericAPIView,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)