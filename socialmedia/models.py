from django.db import models
# from django.db.models.fields import ArrayField
# from django.contrib.postgres.fields import ArrayField

# Create your models here.
class UserProfile(models.Model):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    profession = models.CharField(max_length=100, null=True)
    profile_photo = models.ImageField(upload_to="profile_pics/", null=True)
    about_user = models.CharField(max_length=1000, null=True)

    def save(self, *args, **kwargs):
        # If the instance already exists, check if the image field is being updated
        if self.pk:
            # If the image field is being updated, delete the old image
            try:
                old_instance = UserProfile.objects.get(pk=self.pk)
                if old_instance.profile_photo and self.profile_photo != old_instance.profile_photo:
                    # Delete the old image from S3
                    old_instance.profile_photo.delete(save=False)
            except UserProfile.DoesNotExist:
                pass
        super().save(*args,**kwargs)

    def delete(self, *args, **kwargs):
        # Delete the associated file from storage
        if self.profile_photo:
            self.profile_photo.delete(save=False)
        # Call the parent class's delete method
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.username

class UserFollower(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user')
    follower = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='follower')
    timestamp = models.DateTimeField(auto_now_add=True)

class UserPost(models.Model):
    username = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post_title = models.CharField(max_length=200)
    post_content = models.CharField(max_length=5000)
    post_image = models.ImageField(upload_to='post_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    like_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        # If the instance already exists, check if the image field is being updated
        if self.pk:
            try:
                old_instance = UserPost.objects.get(pk=self.pk)
                if old_instance.post_image and old_instance.post_image != self.post_image:
                    # Delete the old image from S3
                    old_instance.post_image.delete(save=False)
            except UserPost.DoesNotExist:
                pass
        # Save the instance
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Delete the associated file from storage
        if self.post_image:
            self.post_image.delete(save=False)
        # Call the parent class's delete method
        super().delete(*args, **kwargs)

    def __str__(self):
        return "USER: "+self.username.username+"  TITLE: "+self.post_title

class Comments(models.Model):
    username = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

class PostLike(models.Model):
    username = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)