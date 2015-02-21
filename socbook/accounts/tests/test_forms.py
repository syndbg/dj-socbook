from django.test import TestCase

from accounts.models import Account
from accounts.forms import AccountSignupForm, PASSWORDS_MISMATCH_ERROR


class AccountSignupFormTests(TestCase):

    def setUp(self):
        self.form = AccountSignupForm()
        self.given_email = 'foo@bar.com'
        self.given_first_name = 'Anton'
        self.given_last_name = 'Antonov'
        self.given_gender = Account.MALE

        self.good_data = {'email': self.given_email, 'first_name': self.given_first_name,
                          'last_name': self.given_last_name, 'gender': self.given_gender,
                          'password1': 'foobar', 'password2': 'foobar'}

    def test_form_gender_default_is_secret(self):
        self.assertEqual(Account.SECRET, self.form.fields['gender'].initial)

    def test_form_clean_password2_with_mismatching_passwords(self):
        bad_data = self.good_data
        bad_data['password1'] = 'potato'
        self.form = AccountSignupForm(bad_data)
        self.assertFalse(self.form.is_valid())
        self.assertEqual(self.form.errors['password2'], [PASSWORDS_MISMATCH_ERROR])

    def test_form_clean_password2_with_matching_passwords(self):
        self.form = AccountSignupForm(self.good_data)
        self.form.is_valid()
        cleaned_password = self.form.clean_password2()
        self.assertEqual('foobar', cleaned_password)

    def test_form_is_not_valid_when_password1_and_password2_mismatch(self):
        bad_data = self.good_data
        bad_data['password1'] = 'potato'
        self.form = AccountSignupForm(bad_data)
        self.assertFalse(self.form.is_valid())

    def test_form_creates_instance_when_given_valid_data(self):
        self.form = AccountSignupForm(self.good_data)
        self.assertTrue(self.form.is_valid())
        account = self.form.save()
        self.assertEqual(account.first_name, self.given_first_name)
        self.assertEqual(account.last_name, self.given_last_name)
        self.assertEqual(account.gender, self.given_gender)
        self.assertEqual(account.email, self.given_email)
