# Generated by Django 4.2.1 on 2023-07-04 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_alter_tguser_tg_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='tguser',
            name='verification_code',
            field=models.CharField(max_length=15, null=True, verbose_name='Код подтверждения'),
        ),
        migrations.AlterField(
            model_name='tguser',
            name='tg_user',
            field=models.CharField(max_length=32, verbose_name='ID пользователя Telegram'),
        ),
    ]
