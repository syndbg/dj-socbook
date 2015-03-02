from django import forms

from accounts.models import Account, Profile


PASSWORDS_MISMATCH_ERROR = 'The two password fields didn\'t match.'


class AccountSignupForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=Account.GENDERS, initial=Account.SECRET, widget=forms.RadioSelect)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput,
                                help_text='The password you will use to login.')
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput,
                                help_text='Enter the same password, for verification.')

    error_messages = {
        'password_mismatch': PASSWORDS_MISMATCH_ERROR,
    }

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'gender']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(self.error_messages['password_mismatch'],
                                        code='password_mismatch',
                                        )
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class AccountSettingsForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'gender']


class PasswordSettingsForm(forms.Form):
    current_password = forms.CharField(label='Current password', widget=forms.PasswordInput(),)
    new_password1 = forms.CharField(label='New password', widget=forms.PasswordInput())
    new_password2 = forms.CharField(label='Confirm new password', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('for_account')
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        if not self.account.check_password(cleaned_data['current_password']):
            self.add_error('current_password', 'Current password mismatch. Please try again!')

        new_password1 = cleaned_data['new_password1']
        new_password2 = cleaned_data['new_password2']
        if new_password1 != new_password2:
            self.add_error('new_password2', 'New passwords don\'t match. Try again!')
        return cleaned_data

    def save(self, commit=True):
        self.account.set_password(self.cleaned_data['new_password2'])
        if commit:
            self.account.save()
        return self.account


# TO-DO: Have a clear idea what it should do
class PictureSettingsForm(forms.Form):
    pass


class FriendsSettingsForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['display_name']
