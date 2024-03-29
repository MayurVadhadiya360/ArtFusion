# Generated by Django 4.1 on 2023-10-27 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_userprofile_followers_userprofile_following_userpost'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='about_user',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profession',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_photo',
            field=models.ImageField(null=True, upload_to='profile_pics/'),
        ),
    ]
