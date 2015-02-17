from django.test import TestCase

from accounts.models import Account


class AccountModelTests(TestCase):

    def setUp(self):
        self.account = Account.objects.create(username='syndbg', first_name='Anton', last_name='Antonov', gender=Account.MALE, email='asd@asd.com')

    def test_instance(self):
        self.assertEqual('Anton', self.account.first_name)
        self.assertEqual('Antonov', self.account.last_name)
        self.assertEqual(Account.MALE, self.account.gender)

    def test_default_instance_gender(self):
        self.account.delete()
        self.account = Account.objects.create(first_name='Anton', last_name='Antonov')
        self.assertEqual(Account.SECRET, self.account.gender)

    def test_is_friend_with_non_friend_other_account(self):
        other_account = Account.objects.create(first_name='Guido', last_name='van Rossum')
        self.assertFalse(self.account.is_friend(other_account))
        self.assertFalse(other_account.is_friend(self.account))

    def test_is_friend_with_friend_account(self):
        other_account = Account.objects.create(first_name='Guido', last_name='van Rossum')
        other_account.friends.add(self.account)
        self.account.friends.add(other_account)
        self.assertTrue(self.account.is_friend(other_account))
        self.assertTrue(other_account.is_friend(self.account))

    def test_befriend_already_friend_account(self):
        other_account = Account.objects.create(username='guido', first_name='Guido', last_name='van Rossum', email='python@python.com')
        other_account.friends.add(self.account)
        self.account.friends.add(other_account)
        before_befriend_friends_count = other_account.friends.count()
        self.account.befriend(other_account)
        after_befriend_friends_count = other_account.friends.count()
        self.assertEqual(before_befriend_friends_count, after_befriend_friends_count)

    def test_befriend_non_friend_other_account(self):
        other_account = Account.objects.create(username='guido', first_name='Guido', last_name='van Rossum', email='python@python.com')
        self.account.befriend(other_account)
        self.assertTrue(self.account.is_friend(other_account))
        self.assertTrue(other_account.is_friend(self.account))
