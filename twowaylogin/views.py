from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth import login
from django.contrib import messages
from .forms import LoginForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

def login_view(request):
    form = LoginForm(request.POST or None)
    context = {
        "form": form
    }
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user_final_qs = User.objects.filter(
                Q(username__iexact=username) |
                Q(email__iexact=username)
            ).distinct().first()

            if check_password(password, user_final_qs.password):
                login(request,user_final_qs)
                return redirect("home")
            else:
                messages.info(request, "invalid credential")
        else:
            messages.error(request, form.errors)
    return render(request, "login.html", context)

def home_view(request):
    return render(request, "home.html",{})