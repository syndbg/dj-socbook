from django import forms

from accounts.models import Account


class AccountSignupForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=Account.GENDERS, widget=forms.RadioSelect)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput,
                                help_text='Enter the same password as above, for verification.')

    error_messages = {
        'password_mismatch': 'The two password fields didn\'t match.',
    }

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'username', 'email', 'gender']

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
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
