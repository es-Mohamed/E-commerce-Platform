from django.shortcuts import render, redirect
from django.utils.translation import activate, get_language
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import translate_url
from items.models import Category, Item
from .forms import Signupform

def set_language_custom(request, language):
    next_url = request.META.get('HTTP_REFERER', '/')
    
    activate(language)
    
    request.session[settings.LANGUAGE_SESSION_KEY] = language
    
    response = HttpResponseRedirect(next_url)
    response.set_cookie(
        settings.LANGUAGE_COOKIE_NAME,
        language,
        max_age=settings.LANGUAGE_COOKIE_AGE,
        path=settings.LANGUAGE_COOKIE_PATH,
        domain=settings.LANGUAGE_COOKIE_DOMAIN,
        secure=settings.LANGUAGE_COOKIE_SECURE or None,
        samesite=settings.LANGUAGE_COOKIE_SAMESITE,
    )
    return response

def index(request):
    items = Item.objects.filter(is_sold=False)[0:8]
    categories = Category.objects.all()
    return render(request, "core/index.html", {
        'categories': categories,
        'items': items
    })

def contact(request):
    return render(request, "core/contact.html")

def Signup(request):
    if request.method == "POST":
        form = Signupform(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/login/")
    else:
        form = Signupform()
    
    return render(request, "core/Signup.html", {
        'form': form
    })

