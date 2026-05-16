from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from .models import UserProfile
from leaderboard.models import Leaderboard


def home(request):
    return render(request, 'home.html')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                Leaderboard.objects.get_or_create(user=user, defaults={'highest_score': 0, 'rank': 0})
                messages.success(request, 'Account created successfully. Now log in.')
                return redirect('login')
            except Exception as e:
                messages.error(request, f'Registration failed: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('game_index')
        else:
            messages.error(request, 'Invalid username or password.')
    form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


@login_required
def profile_view(request):
    Leaderboard.objects.get_or_create(
        user=request.user,
        defaults={'highest_score': 0, 'rank': 0}
    )
    return render(request, 'profile.html', {'user_profile': request.user})
