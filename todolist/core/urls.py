from django.urls import path

from .views import UserCreateView, UserLogin, UserProfileView, ChangePasswordView

urlpatterns = [
    path('signup', UserCreateView.as_view()),
    path('login', UserLogin.as_view()),
    path('profile', UserProfileView.as_view()),
    path('update_password', ChangePasswordView.as_view()),
]
