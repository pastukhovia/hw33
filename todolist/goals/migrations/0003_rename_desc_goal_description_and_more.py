# Generated by Django 4.2.1 on 2023-06-23 08:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0002_goal'),
    ]

    operations = [
        migrations.RenameField(
            model_name='goal',
            old_name='desc',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='goal',
            old_name='deadline',
            new_name='due_date',
        ),
    ]