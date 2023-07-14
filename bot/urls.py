from django.urls import path

from .views import BotVerifyView

urlpatterns = [
    path('verify', BotVerifyView.as_view())
]
