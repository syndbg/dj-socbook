from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from accounts.forms import AccountSignupForm, AccountSettingsForm, PasswordSettingsForm, PictureSettingsForm, FriendsSettingsForm


def signin(request):
    if not request.user.is_authenticated():
        return auth_views.login(request, template_name='signin.html')
    return redirect('activities:activities')


def signup(request):
    if request.method == 'POST':
        form = AccountSignupForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:signin')
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
    account = request.user
    if request.method == 'POST':
        form = AccountSettingsForm(data=request.POST, instance=account)
        if form.is_valid():
            form.save()
    else:
        form = AccountSettingsForm(instance=account, initial={'first_name': account.first_name, 'last_name': account.last_name,
                                                              'email': account.email, 'gender': account.gender})
    return render(request, 'account_settings.html', {'form': form, 'active': 'account_settings'})


@login_required
def password_settings(request):
    account = request.user
    if request.method == 'POST':
        form = PasswordSettingsForm(data=request.POST, for_account=account)
        if form.is_valid():
            form.save()
    else:
        form = PasswordSettingsForm(for_account=account)
    return render(request, 'password_settings.html', {'form': form, 'active': 'password_settings'})


@login_required
def picture_settings(request):
    pass


@login_required
def friends_settings(request):
    account = request.user
    profile = account.profile
    if request.method == 'POST':
        form = FriendsSettingsForm(data=request.POST, instance=profile)
        if form.is_valid():
            form.save()
    else:
        form = FriendsSettingsForm(instance=profile, initial={'display_name': profile.display_name})
    return render(request, 'friends_settings.html', {'form': form, 'active': 'friends_settings'})


@login_required
def profile(request, profile_name):
    pass
