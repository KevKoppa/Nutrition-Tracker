from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.contrib import messages
from .forms import RegisterForm
from datetime import datetime
from django.contrib.auth import views as auth_views

date = datetime.today().date()


def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            login(request, user)
            messages.success(request, 'Form submitted successfully')
            return redirect(reverse('nutrition:food-list/{}'.format(str(date))))
        messages.error(request, 'Error')
    else:
        form = RegisterForm()
    return render(request, 'registration/signup.html', {'form': form, 'date': str(date)})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return render(request, 'registration/logout.html', {'date': str(date)})


class MyLoginView(auth_views.LoginView):
    template_name = 'registration/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "date": str(date)
        })
        return context

