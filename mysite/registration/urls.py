from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "register"

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('logout', views.logout_view, name='logout'),
    path('login', views.MyLoginView.as_view(), name='login'),
]