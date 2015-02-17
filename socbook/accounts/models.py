from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.signals import account_befriended, friend_request_accepted, friend_request_rejected, friend_request_sent, new_profile_created


class Account(AbstractUser):
    MALE, FEMALE, SECRET = range(3)
    GENDERS = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (SECRET, 'Secret'))
    gender = models.SmallIntegerField(choices=GENDERS, default=SECRET)
    birthday = models.DateField(null=True)
    friends = models.ManyToManyField('self', null=True, blank=True)
    location = models.CharField(max_length=75, blank=True)
    site = models.URLField(blank=True)

    AbstractUser._meta.get_field('email')._unique = True

    def befriend(self, other_account):
        """Adds accounts in both accounts' friends fields and emits a signal for Activity and Notification to pick up."""
        if not self.is_friend(other_account):
            self.friends.add(other_account)
            self.friends.save(update_fields=['friends'])
            other_account.friends.add(self)
            other_account.save(update_fields=['friends'])
            account_befriended.send(sender=self.__class__, account=self, other_account=other_account)

    def is_friend(self, other_account):
        return self in other_account.friends and other_account in self.friends

    def send_friend_request(self, to_account):
        FriendRequest.objects.create(from_account=self, to_account=to_account)


class Profile(models.Model):
    account = models.OneToOneField(Account, related_name='profile')
    url = models.URLField(blank=False)

    @receiver(post_save, sender=Account)
    def create_profile(sender, instance, created, **kwargs):
        """Creates a Profile and emits a signal for Activity to pick up and create an Activity and later Notification."""
        if created:
            url = '//{0}'.format(instance.account.username)
            Profile.objects.create(account=instance, url=url)
            new_profile_created.send(sender=instance.__class__, account=instance, url=url)


class FriendRequest(models.Model):
    from_account = models.ForeignKey(Account, related_name='friend_requests_sent')
    to_account = models.ForeignKey(Account, related_name='friend_requests_received')

    PENDING, ACCEPTED, REJECTED = range(3)
    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    )
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=PENDING)

    class Meta:
        unique_together = (('from_account', 'to_account'),)

    @receiver(post_save, sender='accounts.FriendRequest')
    def send_notification_signal(sender, instance, created, **kwargs):
        """Emits a friend_request_sent signal for Notification to pick up."""
        if created:
            friend_request_sent.send(sender=instance.__class__, from_account=instance.from_account, to_account=instance.to_account)

    def accept(self):
        """Accepts a FriendRequest, befriends from_account and to_account, emits an account_befriended signal
           for Activity to pick up and emits a friend_request_accepted signal for Notification to pick up."""
        self.status = self.ACCEPTED
        self.save(update_fields=['status'])
        self.from_account.befriend(self.to_account)
        friend_request_accepted.send(sender=self.__class__, from_account=self.from_account, to_account=self.to_account)

    def reject(self):
        """Rejects a FriendRequest and emits a friend_request_rejected signal for Notification to pick up"""
        self.status = self.REJECTED
        self.save(update_fields=['status'])
        friend_request_rejected.send(sender=self.__class__, from_account=self.from_account, to_account=self.to_account)
