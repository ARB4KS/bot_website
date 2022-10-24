from django.urls import path
from oauth2discord import views

urlpatterns = [
    path('', views.home, name='oauth2'),
    path('login/', views.discord_login, name='oauth_login'),
    path('login/redirect/', views.discord_login_redirect, name='discord_login_redirect'),
]
