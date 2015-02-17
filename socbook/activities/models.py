from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.signals import account_befriended, friend_request_accepted, friend_request_sent, new_profile_created
from feeds.models import Publication


class Activity(models.Model):
    LIKE, COMMENT, BEFRIEND, PUBLISH, SHARE, REGISTER, = range(5)
    TYPE_CHOICES = (
        (LIKE, 'like'),
        (COMMENT, 'comment'),
        (BEFRIEND, 'befriendment'),
        (PUBLISH, 'publication'),
        (SHARE, 'shared'),
        (REGISTER, 'register'),
    )
    type = models.SmallIntegerField(choices=TYPE_CHOICES, default=LIKE)
    account = models.ForeignKey('accounts.Account', related_name='activities')
    date = models.DateTimeField(auto_now_add=True)

    STR_TEMPLATES = {
        Activity.LIKE: '{account} liked {author}\'s {publication}',
        Activity.COMMENT: '{account} commented on {author}\'s {publication}',
        Activity.BEFRIEND: '{account} became friends with {other_account}',
        # Activity.PUBLISH: '{account} posted {publication}',
        Activity.SHARE: '{account} shared {author}\'s {publication}',
        Activity.REGISTER: '{account} joined the network!',
    }

    # to one of them
    to_account = models.ForeignKey('accounts.Account', null=True, related_name='foreign_activities')
    to_publication = models.ForeignKey('feeds.Publication', null=True, related_name='activities')
    visibility = models.SmallIntegerField(
        choices=Publication.VISIBILITY_CHOICES, default=Publication.FRIENDS)

    @receiver(new_profile_created, sender='accounts.Profile')
    def create_new_profile_created_notification(sender, account):
        Activity.objects.create(type=Activity.REGISTER, account=account, visibility=Publication.PUBLIC)

    @receiver(account_befriended, sender='accounts.Account')
    def create_account_befriended(sender, account, other_account):
        Activity.objects.create(type=Activity.BEFRIEND, account=account, to_account=other_account, visibility=Publication.PUBLIC)


class Notification(models.Model):
    account = models.ForeignKey('accounts.Account', related_name='notifications')
    date = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
    type = models.SmallIntegerField(choices=Activity.TYPE_CHOICES, default=Activity.LIKE)

    STR_TEMPLATES = {
        Activity.LIKE: '{profile} liked {to_profile}\'s {activity_type}',
        Activity.COMMENT: '{profile} commented on {to_profile}\'s {activity_type}',
        Activity.BEFRIEND: '{profile} befriended {to_profile}',
        Activity.PUBLISH: '{profile} published {to_publication}',
        Activity.PROFILE_POST: '{profile} posted on {to_profile}\'s profile',
        Activity.DELETE: 'You have deleted your {activity_type}',
    }

    def __str__(self):
        str_representation = 'Unknown activity type'
        if self.type == Activity.LIKE:
            str_representation = self.STR_TEMPLATES[Activity.LIKE].format(profile=self.activity.profile,
                                                                          to_profile=self.activity.to_profile,
                                                                          activity_type=self.activity.type)
        elif self.type == Activity.COMMENT:
            str_representation = self.STR_TEMPLATES[Activity.COMMENT].format(profile=self.activity.profile,
                                                                             to_profile=self.activity.to_profile,
                                                                             activity_type=self.activity.type)
        elif self.type == Activity.BEFRIEND:
            str_representation = self.STR_TEMPLATES[Activity.BEFRIEND].format(profile=self.activity.profile,
                                                                              to_profile=self.activity.to_profile)
        elif self.type == Activity.PUBLISH:
            str_representation = self.STR_TEMPLATES[Activity.PUBLISH].format(profile=self.activity.profile,
                                                                             to_publication=self.activity.to_publication)
        elif self.type == Activity.PROFILE_POST:
            str_representation = self.STR_TEMPLATES[Activity.PROFILE_POST].format(profile=self.activity.profile,
                                                                                  to_profile=self.activity.to_profile)
        elif self.type == Activity.DELETE:
            str_representation = self.STR_TEMPLATES[Activity.DELETE].format(activity_type=self.activity.type)
        return str_representation
