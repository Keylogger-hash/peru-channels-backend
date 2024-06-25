from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from .views import UserList, UserDetail, UserRegister

app_name = 'authentication'
urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/users/list/', UserList.as_view(), name='user_list'),
    path('api/users/<int:pk>/', UserDetail.as_view(), name='user_detail'),
    path('api/users/register/', UserRegister.as_view(), name='user_register')

]