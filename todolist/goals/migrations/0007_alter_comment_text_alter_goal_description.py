# Generated by Django 4.2.1 on 2023-06-28 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0006_alter_goal_due_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(verbose_name='Текст'),
        ),
        migrations.AlterField(
            model_name='goal',
            name='description',
            field=models.TextField(verbose_name='Описание'),
        ),
    ]
