# Generated by Django 4.2.1 on 2023-07-04 05:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TgUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tg_chat', models.PositiveIntegerField(verbose_name='ID чата Telegram')),
                ('tg_user', models.PositiveIntegerField(verbose_name='ID пользователя Telegram')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='ID пользователя')),
            ],
        ),
    ]
