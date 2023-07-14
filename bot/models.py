from django.db import models

from core.models import User


class TgUser(models.Model):
    tg_chat = models.PositiveIntegerField(verbose_name='ID чата Telegram')
    tg_user = models.CharField(verbose_name='ID пользователя Telegram', max_length=32)
    verification_code = models.CharField(verbose_name='Код подтверждения', max_length=15, null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.PROTECT, verbose_name='ID пользователя')
