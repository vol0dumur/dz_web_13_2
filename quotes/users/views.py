from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import RegisterForm, LoginForm, UserUpdateEmailForm

# Create your views here.
from django.shortcuts import render, redirect

from .forms import RegisterForm


def signupuser(request):
    if request.user.is_authenticated:
        return redirect(to='quoteapp:main')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quoteapp:main')
        else:
            return render(request, 'users/signup.html', context={"form": form})

    return render(request, 'users/signup.html', context={"form": RegisterForm()})


def loginuser(request):
    if request.user.is_authenticated:
        return redirect(to='quoteapp:main')

    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is None:
            messages.error(request, 'Username or password didn\'t match')
            return redirect(to='users:login')

        login(request, user)
        return redirect(to='quoteapp:main')

    return render(request, 'users/login.html', context={"form": LoginForm()})


@login_required
def logoutuser(request):
    logout(request)
    return redirect(to='quoteapp:main')


@login_required
def profile(request):
    if request.method == "POST":
        form = UserUpdateEmailForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("users:profile")
    else:
        form = UserUpdateEmailForm(instance=request.user)

    return render(request, "users/profile.html", {"form": form})
# def profile(request):
#     if request.method == 'POST':
#         profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
#         if profile_form.is_valid():
#             profile_form.save()
#             messages.success(request, 'Your profile is updated successfully')
#             return redirect(to='users:profile')

#     profile_form = ProfileForm(instance=request.user.profile)
#     return render(request, 'users/profile.html', {'profile_form': profile_form})