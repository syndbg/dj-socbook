from django.test import TestCase

from accounts.models import Account


class AccountModelTests(TestCase):

    def setUp(self):
        self.account = Account.objects.create(first_name='Anton', last_name='Antonov', gender=Account.MALE)

    def test_instance(self):
        self.assertEqual('Anton', self.account.first_name)
        self.assertEqual('Antonov', self.account.last_name)
        self.assertEqual(Account.MALE, self.account.gender)

    def test_default_instance_gender(self):
        self.account.delete()
        self.account = Account.objects.create(first_name='Anton', last_name='Antonov')
        self.assertEqual(Account.SECRET, self.account.gender)
