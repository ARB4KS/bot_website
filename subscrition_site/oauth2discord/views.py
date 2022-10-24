from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import requests
from django.contrib.auth.decorators import  login_required




API_ENDPOINT = 'https://discord.com/api/v10'
CLIENT_ID = '1033667474241093693'
CLIENT_SECRET = 'TybyeWQwm59sImj8ZhKhtQKvg6mz4e5p'
REDIRECT_URI = 'http://127.0.0.1:8000/oauth2/login/redirect/'
SERVER_ID = "939513182505037894"

# Create your views here.

#auth_url_discord = "https://discord.com/api/oauth2/authorize?client_id=1033667474241093693&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Foauth2%2Flogin%2Fredirect%2F&response_type=code&scope=identify"
auth_url_discord = "https://discord.com/api/oauth2/authorize?client_id=1033667474241093693&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Foauth2%2Flogin%2Fredirect%2F&response_type=code&scope=identify%20guilds"
def home(request: HttpRequest) -> JsonResponse:
  return JsonResponse({ "msg": "Hello World" })


@login_required(login_url="/oauth2/login/")
def get_authenticated_user(request:HttpRequest):
    return JsonResponse({"msg":"Authenticated"})

def discord_login(request: HttpRequest):
  return redirect(auth_url_discord)

def discord_login_redirect(request: HttpRequest):
  code = request.GET.get('code')
  print("code=",code)
  user = exchange_code(code)
  discord_user = authenticate(request, user=user)
  user_pop = list(discord_user).pop()
  print(user_pop)
  login(request,user_pop)
  #return redirect("/auth/user")
  return HttpResponse(f"<h1>Logged as {user}<h1>")


def exchange_code(code: str):
    data = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': REDIRECT_URI,
        }
    headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    r = requests.post('%s/oauth2/token' % API_ENDPOINT, data=data, headers=headers)
    json = r.json()
    print(json)
    access_token = json["access_token"]
    response = requests.get("https://discord.com/api/v6/users/@me",headers={'Authorization': 'Bearer %s'%access_token})
    response_guild = requests.get("https://discord.com/api/v6/users/@me/guilds",
                            headers={'Authorization': 'Bearer %s' % access_token})
    guilds =response_guild.json()
    user = response.json()
    serveur_id =[]
    for serveur in guilds:
        serveur_id.append(serveur["id"])
    if SERVER_ID in serveur_id:
        return user
    else:
        return "Not logged, you have to join the server"


def view_that_asks_for_money(request):

    # What you want the button to do.
    paypal_dict = {
        "business": "receiver_email@example.com",
        "amount": "10000000.00",
        "item_name": "name of the item",
        "invoice": "unique-invoice-id",
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('your-return-view')),
        "cancel_return": request.build_absolute_uri(reverse('your-cancel-view')),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "payment.html", context)


