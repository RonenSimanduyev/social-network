from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    user = models.OneToOneField(User,on_delete=models.CASCADE ,related_name ='user')  
    city = models.CharField(max_length=200,blank=True,default='')
    dob = models.DateField(max_length=200)
    profile_img = models.CharField(max_length=800,blank=True,default='')
    background_img = models.CharField(max_length=800,blank=True,default='')
    relationship = models.BooleanField(default=False )
    friends = models.ManyToManyField(User ,blank=True ,related_name ='friends' )

    def __str__(self):
        return (self.first_name + " " + self.last_name )


class Group(models.Model):
    user =models.ForeignKey(Profile,on_delete=models.CASCADE ,related_name ='group.user+')
    owner =models.ForeignKey(Profile,on_delete=models.CASCADE ,related_name ='owner')
    description= models.CharField(max_length=400)
    users =models.ManyToManyField(Profile,blank=True,related_name='groupUser')

class Post(models.Model):
    user =models.ForeignKey(Profile,on_delete=models.SET_NULL, null=True,related_name ='postOwner')
    group =models.ForeignKey(Group,on_delete=models.SET_NULL, null=True, blank=True ,related_name ='groupFrieds')
    body = models.TextField()
    likes = models.ManyToManyField(Profile,blank=True,related_name='like')
    created = models.DateTimeField(auto_now_add=True)
    post_img = models.CharField(max_length=800,blank=True,default='')


class Comment(models.Model):
    user =models.ForeignKey(Profile,on_delete=models.SET_NULL, null=True,related_name ='comment')
    post =models.ForeignKey(Post,on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
