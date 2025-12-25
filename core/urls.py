from django.contrib.auth import views as auth_Views
from django.urls import path

from . import views

from .forms import Loginform

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path("contact/", views.contact, name="contact"),
    path("Signup/", views.Signup, name="Signup"),
    path('login/',auth_Views.LoginView.as_view(template_name="core/login.html", authentication_form=Loginform), name='login'),

]
