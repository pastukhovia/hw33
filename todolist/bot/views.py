from rest_framework.generics import UpdateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated

from .management.commands.runbot import tg_client
from .models import TgUser
from .serializers import TgUserUpdateSerializer


class BotVerifyView(UpdateAPIView):
    model = TgUser
    serializer_class = TgUserUpdateSerializer
    permission_classes = [IsAuthenticated, ]

    def get_object(self):
        return get_object_or_404(TgUser, verification_code=self.request.data['verification_code'])

    def perform_update(self, serializer):
        serializer.save()
        tg_client.send_message(chat_id=self.get_object().tg_chat, text='Аккаунт подтвержден')
