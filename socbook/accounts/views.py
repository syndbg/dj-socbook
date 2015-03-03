from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from accounts.forms import AccountSignupForm, AccountSettingsForm, PasswordSettingsForm, PictureSettingsForm, FriendsSettingsForm
from website.utils import form_fields_to_json


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
        json_form_fields = form_fields_to_json(form)
        return render(request, 'signup.html', {'form': form, 'json_form_fields': json_form_fields})
    form = AccountSignupForm()
    json_form_fields = form_fields_to_json(form)
    return render(request, 'signup.html', {'form': form, 'json_form_fields': json_form_fields})


@login_required
def signout(request):
    auth_views.logout(request)
    return redirect('/')


@login_required
def account_settings(request):
    account = request.user
    if request.method == 'POST':
        form = AccountSettingsForm(data=request.POST, instance=account)
        if form.is_valid() and form.has_changed():
            form.save()
            messages.success(request, 'You\'ve updated your account successfully!')
    else:
        form = AccountSettingsForm(instance=account, initial={'first_name': account.first_name, 'last_name': account.last_name,
                                                              'email': account.email, 'gender': account.gender})
    return render(request, 'account_settings.html', {'form': form, 'active': 'account_settings'})


@login_required
def password_settings(request):
    account = request.user
    if request.method == 'POST':
        form = PasswordSettingsForm(data=request.POST, for_account=account)
        if form.is_valid() and form.has_changed():
            form.save()
            messages.success(request, 'You\'ve updated your password successfully!')
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
        if form.is_valid() and form.has_changed():
            form.save()
            messages.success(request, 'You\'ve updated your display_name successfully!')
    else:
        form = FriendsSettingsForm(instance=profile, initial={'display_name': profile.display_name})
    return render(request, 'friends_settings.html', {'form': form, 'active': 'friends_settings'})


@login_required
def profile(request, profile_name):
    pass
