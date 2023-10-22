from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

User = get_user_model()


# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='profile')
    id_user = models.IntegerField()
    bio = models.TextField(max_length=20000,blank=True) 
    location = models.CharField(max_length=200,blank=True)
    profileimg = models.ImageField(upload_to='profile_images',default='blank-profile-picture.png')


    def __str__(self):
        return self.user.username



class Post(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='posts')
    image=models.ImageField(upload_to='post_images')
    caption=models.TextField()
    created_at=models.DateTimeField(default=datetime.now)
    no_of_likes=models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)
    
class Comment(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='comments')
    usr_comment=models.TextField()
    created_at=models.DateTimeField(default=datetime.now)
    
    def __str__(self):
        return self.profile
    
class LikePost(models.Model):
    post_id=models.CharField(max_length=20000)
    username=models.CharField(max_length=100)
    
    def __str__(self):
        return self.username
    

class FollowedCount(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='followers')
    following=models.ForeignKey(User,on_delete=models.CASCADE,related_name='following')