# Generated by Django 5.0.6 on 2024-05-15 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vkr', '0004_usersubscribe_user_name_alter_usersubscribe_user_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usersubscribe',
            name='id',
        ),
        migrations.AlterField(
            model_name='usersubscribe',
            name='user_id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
