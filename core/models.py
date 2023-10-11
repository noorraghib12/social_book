from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.cascade)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=200,blank=True)
    profileimg = models.ImageField(upload_to='profile_images',default='blank-profile-picture.png')


    def __str__(self):
        return self.user.username

