# HttpResponse Related
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest, JsonResponse

# Database Related
from .models import CustomUser
from django.db.models import Q

# Authentication Related
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

# Json Serializer
from django.core import serializers


# Create your views here.
def index(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            if request.user.is_profileComplete == False:
                return render(request, "complete_profile.html", {"fullname": request.user.full_name.split(" ")[0]})
            return render(request, "index.html")
        else:
            return redirect("signin")
    return HttpResponseBadRequest("[!] Method Not Allowed !!!")
    

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.error(request, "[!] Email or Password invalid.")
    return render(request, "signin.html")


def signup(request):
    if request.method == "POST":
        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not full_name:
            messages.error(request, "[!] Full Name is required.")
            return redirect("signup")

        if not username:
            messages.error(request, "[!] Email or Phone is required.")
            return redirect("signup")

        if CustomUser.objects.filter(email_or_phone=username).exists():
            messages.error(request, "[!] Email already exists.")
            return redirect("signup")
        else:
            if len(password) < 8:
                messages.error(request, "[!] Minimum Password length is 8.")
                return redirect("signup")
            obj = CustomUser(email_or_phone=username, password=make_password(password), full_name=full_name)
            obj.save()
            messages.success(request, "[*] Registration Successful, Please Login !!!")
            return redirect("signin")
    return render(request, "signup.html")


def signout(request):
    user = request.user
    try:
        frnd = CustomUser.objects.get(email_or_phone=user.connected_with)
        frnd.connected_with = ""
        frnd.save()
    except:
        pass

    user.connected_with = ""
    user.online_status = False
    user.save()

    logout(request)
    return redirect("signin")


def complete_profile(request):
    if request.method == "POST":
        gender = request.POST.get('gender')
        country = request.POST.get('country')
        interests = request.POST.get('interests')

        if not gender:
            messages.error(request, "[!] Gender is required.")
            return redirect("index")
        elif not country or country == "":
            messages.error(request, "[!] Country is required.")
            return redirect("index")
        elif not interests:
            messages.error(request, "[!] Interests is required.")
            return redirect("index")
        else:
            obj = CustomUser.objects.get(email_or_phone=request.user.email_or_phone)
            obj.country = country
            obj.gender = gender
            obj.interests = interests
            obj.is_profileComplete = True
            obj.save()
            return redirect("index")
    return HttpResponseBadRequest("[!] Method Not Allowed !!!")    


@csrf_exempt
def change_online_status(request):
    user = request.user
    user.online_status = request.POST.get('online_status') == "true"
    user.save()
    return JsonResponse({"msg": "Done"})

def chat_window(request):
    if request.user.is_authenticated and request.user.online_status == True:
        frnd = CustomUser.objects.get(email_or_phone=request.user.connected_with)
        return render(request, "chat_window.html", {"frnd_name": frnd.full_name, "frnd_email":request.user.connected_with})

    return HttpResponseBadRequest("[!] You're not authenticated !!!")