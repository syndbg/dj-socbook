from django.test import TestCase

from accounts.models import Account
from activities.models import ActivityManager, Activity, Notification
from feeds.models import Publication
from profiles.models import Profile


class ActivityManagerTests(TestCase):

    def setUp(self):
        self.manager = ActivityManager()
        self.account = Account.objects.create(
            first_name='Anton', last_name='Antonov', gender=Account.MALE)
        self.profile = Profile.objects.last()
        self.activity = Activity.objects.create(
            type=Activity.LIKE, profile=self.profile)
        self.to_activity = Activity.objects.create(
            type=Activity.LIKE, profile=self.profile, to_activity=self.activity)
        self.publication = Publication.objects.create(author=self.profile)

    def test_invalid_activity_with_no_profile(self):
        with self.assertRaises(ValueError):
            self.manager.comment(None, '', self.activity, None)

    def test_invalid_activity_regarding_more_than_one(self):
        with self.assertRaises(ValueError):

            self.manager.comment(
                self.profile, 'Kappa', self.to_activity, self.publication)

    def test_invalid_activity_regarding_none(self):
        with self.assertRaises(ValueError):
            self.manager.like(self.profile, None, None)

    def test_invalid_comment_with_no_content(self):
        with self.assertRaises(ValueError):
            self.manager.comment(self.profile, '', None, None)

    def test_invalid_profile_post_with_no_content(self):
        with self.assertRaises(ValueError):
            self.manager.profile_post(self.profile, '', self.profile)

    def test_like_to_activity(self):
        pre_count = Activity.objects.count()
        activity = self.manager.like(self.profile, to_activity=self.activity)
        after_count = Activity.objects.count()

        self.assertEqual(after_count, pre_count + 1)
        self.assertIs(self.profile, activity.profile)
        self.assertIs(self.activity, activity.to_activity)
        self.assertEqual(Activity.LIKE, activity.type)

    def test_like_to_publication(self):
        pre_count = Activity.objects.count()
        activity = self.manager.like(self.profile, to_publication=self.publication)
        after_count = Activity.objects.count()

        self.assertEqual(after_count, pre_count + 1)
        self.assertIs(self.profile, activity.profile)
        self.assertIs(self.publication, activity.to_publication)
        self.assertEqual(Activity.LIKE, activity.type)

    def test_comment_to_activity(self):
        pre_count = Activity.objects.count()
        activity = self.manager.comment(self.profile, content='Kappa', to_activity=self.activity)
        after_count = Activity.objects.count()

        self.assertEqual(after_count, pre_count + 1)
        self.assertIs(self.profile, activity.profile)
        self.assertIs(self.activity, activity.to_activity)
        self.assertEqual(Activity.COMMENT, activity.type)

    def test_comment_to_publication(self):
        pre_count = Activity.objects.count()
        activity = self.manager.comment(self.profile, content='Kappa', to_publication=self.publication)
        after_count = Activity.objects.count()

        self.assertEqual(after_count, pre_count + 1)
        self.assertIs(self.profile, activity.profile)
        self.assertIs(self.publication, activity.to_publication)
        self.assertEqual(Activity.COMMENT, activity.type)

    def test_profile_post_to_profile(self):
        pre_count = Activity.objects.count()
        content = 'Kappa'
        activity = self.manager.profile_post(self.profile, content=content, to_profile=self.profile)
        after_count = Activity.objects.count()

        self.assertEqual(after_count, pre_count + 1)
        self.assertEqual(self.profile, activity.profile)
        self.assertEqual(self.profile, activity.to_profile)


class ActivityModelTests(TestCase):

    def setUp(self):
        self.account = Account.objects.create(
            first_name='Anton', last_name='Antonov', gender=Account.MALE)
        self.profile = Profile.objects.last()

    def test_instance(self):
        pass
