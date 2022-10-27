from django.db import models
from .managers import DiscordUserOauth2Manager
import random
# Create your models here.
class DiscordUser(models.Model):
    objects = DiscordUserOauth2Manager()
    id = models.BigIntegerField(primary_key=True)
    discord_tag = models.CharField(max_length=100)
    avatar = models.CharField(max_length=100)
    public_flags = models.IntegerField()
    locale=models.CharField(max_length=100)
    mfa_enabled = models.BooleanField()
    last_login = models.DateTimeField(null=True)
    secret_key = models.CharField(max_length=100,null=True)


    def is_authenticated(self,request):
        return True