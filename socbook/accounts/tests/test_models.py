from django.test import TestCase

from accounts.models import Account, Profile, FriendRequest


class AccountModelTests(TestCase):

    def setUp(self):
        self.account = Account.objects.create(username='syndbg', first_name='Anton', last_name='Antonov', gender=Account.MALE, email='asd@asd.com')
        self.other_account = Account.objects.create(username='guido', first_name='Guido', last_name='van Rossum', email='python@python.com')

    def test_instance(self):
        self.assertEqual('Anton', self.account.first_name)
        self.assertEqual('Antonov', self.account.last_name)
        self.assertEqual(Account.MALE, self.account.gender)

    def test_default_instance_gender(self):
        self.account.delete()
        self.account = Account.objects.create(first_name='Anton', last_name='Antonov')
        self.assertEqual(Account.SECRET, self.account.gender)

    def test_is_friend_with_non_friend_other_account(self):
        self.assertFalse(self.account.is_friend(self.other_account))
        self.assertFalse(self.other_account.is_friend(self.account))

    def test_is_friend_with_friend_account(self):
        self.other_account.friends.add(self.account)
        self.account.friends.add(self.other_account)
        self.assertTrue(self.account.is_friend(self.other_account))
        self.assertTrue(self.other_account.is_friend(self.account))

    def test_befriend_already_friend_account(self):
        self.other_account.friends.add(self.account)
        self.account.friends.add(self.other_account)
        before_befriend_friends_count = self.other_account.friends.count()
        self.account.befriend(self.other_account)
        after_befriend_friends_count = self.other_account.friends.count()
        self.assertEqual(before_befriend_friends_count, after_befriend_friends_count)

    def test_befriend_non_friend_other_account(self):
        self.account.befriend(self.other_account)
        self.assertTrue(self.account.is_friend(self.other_account))
        self.assertTrue(self.other_account.is_friend(self.account))

    def test_unfriend_when_is_not_friend(self):
        self.assertFalse(self.account.is_friend(self.other_account))
        self.account.unfriend(self.other_account)
        self.assertFalse(self.account.is_friend(self.other_account))

    def test_unfriend_when_is_friend(self):
        self.account.befriend(self.other_account)
        self.assertTrue(self.account.is_friend(self.other_account))
        self.account.unfriend(self.other_account)
        self.assertFalse(self.account.is_friend(self.other_account))

    def test_send_friend_request(self):
        before_friend_requests_count = FriendRequest.objects.count()
        friend_request = self.account.send_friend_request(self.other_account)
        after_friend_requests_count = FriendRequest.objects.count()

        self.assertIs(self.account, friend_request.from_account)
        self.assertIs(self.other_account, friend_request.to_account)
        self.assertEqual(after_friend_requests_count, before_friend_requests_count + 1)

    def test_send_friend_request_when_already_sent(self):
        self.account.send_friend_request(self.other_account)
        with self.assertRaises(ValueError):
            self.account.send_friend_request(self.other_account)


class ProfileModelTests(TestCase):

    def test_creates_profile_on_account_post_save_signal(self):
        before_profile_count = Profile.objects.count()
        Account.objects.create(username='syndbg', first_name='Anton', last_name='Antonov', gender=Account.MALE, email='asd@asd.com')
        Profile.objects.last()
        after_profile_count = Profile.objects.count()
        self.assertEqual(after_profile_count, before_profile_count + 1)


class FriendRequestModelTests(TestCase):

    def setUp(self):
        self.account = Account.objects.create(username='syndbg', first_name='Anton', last_name='Antonov', gender=Account.MALE, email='asd@asd.com')
        self.other_account = Account.objects.create(username='guido', first_name='Guido', last_name='van Rossum', email='python@python.com')
        self.friend_request = FriendRequest.objects.create(from_account=self.account, to_account=self.other_account)

    def test_instance_default_status_is_PENDING(self):
        self.assertEqual(FriendRequest.PENDING, self.friend_request.status)

    def test_accept_friend_request(self):
        self.assertNotEqual(FriendRequest.ACCEPTED, self.friend_request.status)

        self.friend_request.accept()
        self.assertTrue(self.account.is_friend(self.other_account))
        self.assertEqual(FriendRequest.ACCEPTED, self.friend_request.status)

    def test_reject_friend_request(self):
        self.assertNotEqual(FriendRequest.REJECTED, self.friend_request.status)

        self.friend_request.reject()
        self.assertFalse(self.account.is_friend(self.other_account))
        self.assertEqual(FriendRequest.REJECTED, self.friend_request.status)
