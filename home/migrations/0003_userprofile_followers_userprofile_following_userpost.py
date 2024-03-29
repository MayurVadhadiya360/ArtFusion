# Generated by Django 4.1 on 2023-10-25 04:39

from django.db import migrations, models
import django.db.models.deletion
import home.models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='followers',
            field=models.JSONField(default=home.models.JsonDefaultFollowers, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='following',
            field=models.JSONField(default=home.models.JsonDefaultFollowing, null=True),
        ),
        migrations.CreateModel(
            name='UserPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_title', models.CharField(max_length=200)),
                ('post_content', models.CharField(max_length=1000)),
                ('post_image', models.ImageField(upload_to='post_images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('likes', models.JSONField(default=home.models.JsonDefaultLike, null=True)),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.userprofile')),
            ],
        ),
    ]
