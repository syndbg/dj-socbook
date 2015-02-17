from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.signals import account_befriended, friend_request_accepted, friend_request_sent, friend_request_rejected, new_profile_created
from feeds.models import Publication


class Activity(models.Model):
    LIKE, COMMENT, BEFRIEND, PUBLISH, SHARE, REGISTER, = range(6)
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
        LIKE: '<a href="{account_url}">{account}</a> liked <a href="{author_url}">{author}\'s</a> <a href="{publication_url}">{publication}</a>',
        COMMENT: '<a href="{account_url}">{account}</a> commented on <a href="{author_url}">{author}\'s</a> <a href="{publication_url}">{publication}</a>',
        BEFRIEND: '<a href="{account_url}">{account}</a> became friends with <a href="other_account_url}">{other_account}</a>',
        # TO-DO: Activity.PUBLISH: '{account} posted {publication}',
        SHARE: '<a href="{account_url}">{account}</a> shared <a href="{author_url}">{author}\'s</a> <a href="{publication_url}">{publication}</a>',
        REGISTER: '<a href="{account_url}">{account}</a> joined the network!',
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

    # TO-DO after Publication
    # def __str__(self):
    #     str_representation = self.STR_TEMPLATES.get(self.type, 'Unknown activity type')
    #     if self.type == Activity.LIKE or self.type == Activity.COMMENT or self.type == Activity.SHARE:
    #         account_url = account.profile.url
    #         str_representation.format(account_url=account.profile.url)
    #     return str_representation


class Notification(models.Model):
    from_account = models.ForeignKey('accounts.Account', related_name='+')
    to_account = models.ForeignKey('accounts.Account', related_name='notifications')
    date = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

    LIKE, COMMENT, PUBLISH, SHARE, REGISTER, FRIEND_REQUEST_ACCEPTED, FRIEND_REQUEST_SENT, FRIEND_REQUEST_REJECTED = range(8)
    TYPE_CHOICES = (
        (LIKE, 'like'),
        (COMMENT, 'comment'),
        (PUBLISH, 'publication'),
        (SHARE, 'shared'),
        (REGISTER, 'register'),
        (FRIEND_REQUEST_ACCEPTED, 'friend request acceptence'),
        (FRIEND_REQUEST_SENT, 'friend request transmission'),
        (FRIEND_REQUEST_REJECTED, 'friend request rejectection'),
    )
    type = models.SmallIntegerField(choices=TYPE_CHOICES, default=TYPE_CHOICES.LIKE)

    # regarding one of them
    publication = models.ForeignKey('feeds.Publication', null=True)
    activity = models.ForeignKey(Activity, null=True)  # TO-DO: as in future Tagging?
    STR_TEMPLATES = {
        LIKE: '<a href="{from_profile_url}">{from_profile}</a> liked your <a href="{publication_url}">{publication_type}<a/>',
        COMMENT: '<a href="{from_profile_url}">{from_profile}</a> commented on your <a href="{publication_url}">{publication_type}<a/>',
        # PUBLISH: '{profile} published {to_publication}',
        SHARE: '<a href="{from_profile_url}">{from_profile}</a> shared your <a href="{publication_url}">{publication_type}<a/>',
        REGISTER: 'You joined the network! Welcome!',
        FRIEND_REQUEST_ACCEPTED: '<a href="{from_profile_url}">{from_profile}</a> accepted your friend request.',
        FRIEND_REQUEST_REJECTED: '<a href="{from_profile_url}">{from_profile}</a> rejected your friend request.',
    }

    @receiver(friend_request_sent, sender='accounts.FriendRequest')
    def create_friend_request_sent_notification(sender, from_account, to_account):
        Notification.objects.create(from_account=from_account, to_account=to_account, type=Notification.FRIEND_REQUEST_SENT)

    @receiver(friend_request_accepted, sender='accounts.FriendRequest')
    def create_friend_requst_accepted_notification(sender, from_account, to_account):
        Notification.objects.create(from_account=from_account, to_account=to_account, type=Notification.FRIEND_REQUEST_ACCEPTED)

    @receiver(friend_request_rejected, sender='accounts.FriendRequest')
    def create_friend_request_rejected_notification(sender, from_account, to_account):
        Notification.objects.create(from_account=from_account, to_account=to_account, type=Notification.FRIEND_REQUEST_REJECTED)

    # TO-DO after Publication
    def __str__(self):
        pass
