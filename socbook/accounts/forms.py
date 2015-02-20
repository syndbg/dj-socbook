from django import forms

from accounts.models import Account


class AccountSignupForm(forms.ModelForm):

    class Meta:
        model = Account
