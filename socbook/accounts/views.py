from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from accounts.forms import AccountSignupForm


def signin(request):
    if not request.user.is_authenticated():
        return auth_views.login(request, template_name='signin.html')
    return redirect('activities:activities')


def signup(request):
    if request.method == 'POST':
        form = AccountSignupForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        return render(request, 'signup.html', {'form': form})
    form = AccountSignupForm()
    return render(request, 'signup.html', {'form': form})


@login_required
def signout(request):
    auth_views.logout(request)
    return redirect('/')


def password_forgotten(request):
    pass


@login_required
def account_settings(request):
    pass


@login_required
def picture_settings(request):
    pass


@login_required
def friends_settings(request):
    pass


@login_required
def password_settings(request):
    pass


@login_required
def profile(request, profile_id):
    pass
