# Generated by Django 4.1.5 on 2023-01-25 11:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0002_rename_userimage_userprofileimage'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserProfileImage',
            new_name='UserProfile',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='user',
            new_name='owner',
        ),
    ]
