from django.core.urlresolvers import reverse
from django.test import TestCase

from accounts.models import Account


class SignTests(TestCase):

    def setUp(self):
        self.account = Account.objects.create_user('user@socbook.com', 'soc')

    def test_signin_uses_auth_views_login_whe_not_authenticated(self):
        response = self.client.get(reverse('accounts:signin'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('signin.html', response)

    # TO-DO: Activities views and urls
    # def test_signin_redirects_to_activities_when_authenticated(self):
    #     self.client.login(username='user@socbook.com', password='soc')
    #     response = self.client.get(reverse('accounts:signin'))
    #     self.assertRedirects(response, reverse('activities:activities'))

    def test_signup_POST_with_invalid_form(self):
        pass

    def test_signup_POST_with_valid_form(self):
        pass

    def test_signup_GET(self):
        pass

    def test_signout_redirects_to_root(self):
        self.client.login(username='user@socbook.com', password='soc')
        self.assertIn('_auth_user_id', self.client.session)
        response = self.client.get(reverse('accounts:signout'))
        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertRedirects(response, '/')


class SettingsViewsTests(TestCase):
    pass
