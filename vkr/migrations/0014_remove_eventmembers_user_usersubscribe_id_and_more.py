# Generated by Django 5.0.6 on 2024-05-17 09:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vkr', '0013_eventmembers_user_prof'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventmembers',
            name='user',
        ),
        migrations.AddField(
            model_name='usersubscribe',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='usersubscribe',
            name='user_id',
            field=models.ForeignKey(blank=True, default=5, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
