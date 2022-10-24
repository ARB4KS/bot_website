from django.contrib.auth.backends import BaseBackend
from .models import DiscordUser

class DiscordAuthenticationBackend(BaseBackend):
    def authenticate(self,request,user)-> DiscordUser:
        print("Executé")
        find_user = DiscordUser.objects.filter(id=user["id"])
        print(find_user)
        if len(find_user)==0:
            new_user = DiscordUser.objects.create_new_discord_user(user)
            print(new_user)
            return new_user
        return find_user


