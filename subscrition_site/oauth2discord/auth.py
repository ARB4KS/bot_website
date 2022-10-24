from django.contrib.auth.backends import BaseBackend
from .models import DiscordUser

class DiscordAuthentificationBackend(BaseBackend):
    def authentificate(self,request,user)-> DiscordUser:
        find_user = DiscordUser.objects.filter(id=user["id"])
        if len(find_user)==user:
            print("User was not found... saving")


