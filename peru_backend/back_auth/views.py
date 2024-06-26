from rest_framework import generics
from rest_framework import mixins
from django.contrib.auth.models import User
from .serializers import UserSerializer, UserRegisterSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User
# Create your views here.


class UserList(
    mixins.ListModelMixin, generics.GenericAPIView
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def get_user_from_access_token_in_django_rest_framework_simplejwt(access_token_str):
    access_token_obj = AccessToken(access_token_str)
    user_id = access_token_obj['user_id']
    user = User.objects.get(id=user_id)
    content = {'id': user.id, 'username': user.username}
    return Response(content)
#Bearer

class UserProfile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        access_token = request.headers.get('Authorization')
        if access_token is not None:
            access_token = access_token.split(' ')[1]
            return get_user_from_access_token_in_django_rest_framework_simplejwt(access_token)
        return Response("Unauthorized",status=status.HTTP_401_UNAUTHORIZED)


class UserRegister(
    generics.GenericAPIView, mixins.CreateModelMixin
):
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = RefreshToken.for_user(user)
        data = serializer.data
        data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
        return Response(data, status=status.HTTP_201_CREATED)


class UserDetail(
    mixins.RetrieveModelMixin,
    generics.GenericAPIView,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class LogoutAPIView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh_token') # С клиента нужно отправить refresh token
        if not refresh_token:
            return Response({'error': 'Необходим Refresh token'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist() # Добавить его в чёрный список
        except Exception as e:
            return Response({'error': 'Неверный Refresh token'},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({'success': 'Выход успешен'}, status=status.HTTP_200_OK)
