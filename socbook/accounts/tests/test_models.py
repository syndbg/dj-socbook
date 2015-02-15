from django.test import TestCase

from accounts.models import Account


class AccountModelTests(TestCase):

    def setUp(self):
        self.account = Account.models.create(first_name='Anton', last_name='Antonov', gender=Account.MALE)

    def test_instance(self):
        self.assertEqual('Anton', self.account.first_name)
        self.assertEqual('Antonov', self.account.last_name)
        self.assertEqual('Male', self.account.gender)
