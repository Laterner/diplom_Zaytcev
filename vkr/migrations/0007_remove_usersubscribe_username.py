# Generated by Django 5.0.6 on 2024-05-15 22:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vkr', '0006_rename_user_name_usersubscribe_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usersubscribe',
            name='username',
        ),
    ]
