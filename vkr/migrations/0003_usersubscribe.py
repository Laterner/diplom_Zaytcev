# Generated by Django 5.0.6 on 2024-05-15 21:35

import django.contrib.auth.models
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vkr', '0002_event'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSubscribe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.TextField(verbose_name=django.contrib.auth.models.User)),
                ('purchase_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('valid_until', models.DateTimeField()),
            ],
        ),
    ]
