from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin


# Create your models here.
class SocialAuth(models.Model):
    """
    To store the token details
    """
    user = models.OneToOneField(User)
    access_token = models.CharField(max_length=100)
    expires_in = models.IntegerField()
    refresh_token = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now=True)


class SocialAuthAdmin(admin.ModelAdmin):
    exclude = None

admin.site.register(SocialAuth, SocialAuthAdmin)
