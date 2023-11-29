from django.db import models
# from django.db.models.fields import ArrayField
# from django.contrib.postgres.fields import ArrayField

# Create your models here.
class CustomUser(models.Model):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username


def JsonDefaultFollowers():
    return {"followers": []}

def JsonDefaultFollowing():
    return {"following": []}

class UserProfile(models.Model):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    profession = models.CharField(max_length=100, null=True)
    profile_photo = models.ImageField(upload_to="profile_pics/", null=True)
    about_user = models.CharField(max_length=1000, null=True)
    # followers = ArrayField(models.CharField(max_length=30), default=list, blank=True)
    # following = ArrayField(models.CharField(max_length=30), default=list, blank=True)
    followers = models.JSONField(null=True, default=JsonDefaultFollowers)
    following = models.JSONField(null=True, default=JsonDefaultFollowing)
    

    def __str__(self):
        return self.username

def JsonDefaultLike():
    return {"likes": []}

def JsonDefaultComment():
    return {"comments": []}

class UserPost(models.Model):
    username = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post_title = models.CharField(max_length=200)
    post_content = models.CharField(max_length=5000)
    post_image = models.ImageField(upload_to='post_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.JSONField(null=True, default=JsonDefaultLike)
    # comments = models.JSONField(null=True, default=JsonDefaultComment)

    def __str__(self):
        return "USER: "+self.username.username+"  TITLE: "+self.post_title

class Comments(models.Model):
    username = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment