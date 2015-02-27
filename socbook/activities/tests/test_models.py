from django.test import TestCase

from accounts.models import Account, Profile
from activities.models import Activity, Notification


class ActivityModelTests(TestCase):

    def setUp(self):
        self.account = Account.objects.create(
            first_name='Anton', last_name='Antonov', gender=Account.MALE)
        self.profile = Profile.objects.last()
        self.activity = Activity.objects.create(profile=self.profile)

    def test_instance_has_default_type_LIKE(self):
        self.assertEqual(Activity.LIKE,  self.activity.type)

    def test_instance_has_date_auto_now_add(self):
        self.assertIsNotNone(self.activity.date)

    def test_instance_has_last_modified_auto_now(self):
        self.assertIsNotNone(self.activity.last_modified)
        previous_last_modified = self.activity.last_modified
        self.activity.type = Activity.DELETE
        self.activity.save()
        self.assertGreater(self.activity.last_modified, previous_last_modified)

    def test_instance_has_default_blank(self):
        self.assertEqual('', self.activity.content)

    def test_invalid_edit_non_comment(self):
        with self.assertRaises(ValueError):
            self.activity.edit('kappa')

    def test_edit_with_no_new_content(self):
        self.activity.type = Activity.COMMENT
        self.activity.content = 'django'
        self.activity.save()

        self.activity.edit('')
        self.assertNotEqual('', self.activity.content)

    def test_edit_comment_with_new_content(self):
        self.activity.type = Activity.COMMENT
        self.activity.save()

        new_content = 'django'
        self.activity.edit(new_content)
        self.assertEqual(new_content, self.activity.content)

    def test_edit_profile_post_with_new_content(self):
        self.activity.type = Activity.PROFILE_POST
        self.activity.save()

        new_content = 'django'
        self.activity.edit(new_content)
        self.assertEqual(new_content, self.activity.content)

    def test_create_notifications(self):
        pre_count = Notification.objects.count()
        new_activity = Activity.objects.create(profile=self.profile, type=Activity.DELETE)
        after_count = Notification.objects.count()
        notification = Notification.objects.last()

        self.assertEqual(after_count, pre_count + 1)
        self.assertEqual(notification.type, new_activity.type)


class NotificationModelTests(TestCase):

    def setUp(self):
        self.account = Account.objects.create(
            first_name='Anton', last_name='Antonov', gender=Account.MALE)
        self.profile = Profile.objects.last()
        self.activity = Activity.objects.create(profile=self.profile)
        self.notification = Notification.objects.last()

    def test_instance_seen_has_default_false(self):
        self.assertFalse(self.notification.seen)

    def test_instance_date_has_default_auto_now_add(self):
        self.assertIsNotNone(self.notification.date)

    def test_instance_has_default_type_like(self):
        self.assertEqual(Activity.LIKE, self.notification.type)

    def test_string_representation_when_type_like(self):
        pass

    def test_string_representation_when_type_comment(self):
        pass

    def test_string_representation_when_type_befriend(self):
        pass

    def test_string_representation_when_type_publish(self):
        pass

    def test_string_representation_when_type_profile_post(self):
        pass

    def test_string_representation_when_type_delete(self):
        pass
