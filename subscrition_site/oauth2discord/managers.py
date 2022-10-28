from django.contrib.auth import models
import random

class DiscordUserOauth2Manager(models.UserManager):
    def create_new_discord_user(self,user):
        discord_tag = "%s#%s" % (user["username"], user["discriminator"])
        print("User was not found... saving")
        new_user = self.create(
            id=user["id"],
            avatar=user["avatar"],
            public_flags=user["public_flags"],
            locale=user["locale"],
            mfa_enabled=user["mfa_enabled"],
            discord_tag=discord_tag,
            secret_key =  random.getrandbits(128)

        )
        return new_user