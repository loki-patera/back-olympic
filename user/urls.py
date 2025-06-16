from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import api

urlpatterns = [
  path('check-email', api.check_email_exists, name='check_email_exists'),
  path('register', api.register_user, name='register_user'),
  path('login', api.CustomTokenObtainPairView.as_view(), name='login'),
  path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
  path('me', api.me, name='me'),
  path('logout', api.logout_user, name='logout_user')
]