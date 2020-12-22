from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Page(models.Model):
    title = models.CharField(max_length=100)
    page_id = models.CharField(max_length=100)
    access_token = models.CharField(max_length=500)
    page_icon = models.CharField(max_length=200,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.PROTECT)
    fb_id = models.CharField(max_length=200)
    fb_token = models.CharField(max_length=500, unique=True)
    profile_image = models.CharField(max_length=200)
    full_name = models.CharField(max_length=100)
    pages = models.ManyToManyField(Page,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
