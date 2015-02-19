from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from accounts.forms import SignupForm


def signin(request):
    if not request.user.is_authenticated():
        return auth_views.login(request, template_name='signin.html')
    return redirect('activities:activities')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    form = SignupForm()
    return render(request, 'signup.html', {'form': form})


@login_required
def signout(request):
    auth_views.logout(request)
    return redirect('/')


@login_required
def settings(request):
    pass


@login_required
def picture_settings(request):
    pass


@login_required
def friend_settings(request):
    pass
