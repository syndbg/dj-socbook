from django.test import TestCase

from accounts.models import Account
from profile.models import Profile


class ProfileModelTests(TestCase):

    def setUp(self):
        self.before_account_count = Profile.objects.count()
        self.account = Account.objects.create(first_name='Anton', last_name='Antonov', gender=Account.MALE)

    def test_creating_an_account_creates_a_profile(self):
        after_account_creation_count = Profile.objects.count()
        self.assertEqual(after_account_creation_count, self.before_account_count + 1)

    def test_deleting_an_account_deletes_the_profile(self):
        self.account.delete()
        after_acount_deletion_count = Profile.objects.count()
        self.assertEqual(self.before_account_count, after_acount_deletion_count)

    def test_profile_instance(self):
        profile = Profile.objects.last()
        self.assertEqual(self.account, profile.account)
        self.assertEqual('', profile.location)
        self.assertEqual([], profile.friends)
