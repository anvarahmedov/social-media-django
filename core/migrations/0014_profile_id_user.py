# Generated by Django 5.1.5 on 2025-02-02 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_profile_following_alter_profile_followers'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='id_user',
            field=models.IntegerField(null=True, unique=True),
        ),
    ]
