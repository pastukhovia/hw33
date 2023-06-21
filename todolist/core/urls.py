from django.urls import path, include

from .views import UserCreateView

urlpatterns = [
    path('signup/', UserCreateView.as_view(), name='signup')
]
