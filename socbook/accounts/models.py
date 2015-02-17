from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.signals import account_befriended, friend_request_accepted, friend_request_rejected, friend_request_sent


class Account(AbstractUser):
    MALE, FEMALE, SECRET = range(3)
    GENDERS = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (SECRET, 'Secret'))
    gender = models.SmallIntegerField(choices=GENDERS, default=SECRET)
    account = models.ForeignKey('accounts.Account')
    birthday = models.DateField(null=True)
    friends = models.ManyToManyField('self', null=True, blank=True)
    location = models.CharField(max_length=75, blank=True)
    site = models.URLField(blank=True)

    AbstractUser._meta.get_field('email')._unique = True

    def befriend(self, other_account):
        if not self.is_friend(other_account):
            self.friends.add(other_account)
            other_account.friends.add(self)
            account_befriended.send(sender=self.__class__, account=self, other_account=other_account)

    def is_friend(self, other_account):
        return self in other_account.friends and other_account in self.friends


class Profile(models.Model):
    account = models.OneToOneField(Account)
    url = models.URLField(blank=False)

    @receiver(post_save, sender=Account)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            url = '//{0}'.format(instance.account.username)
            Profile.objects.create(account=instance, url=url)


class FriendRequest(models.Model):
    from_account = models.ForeignKey(Account)
    to_account = models.ForeignKey(Account)

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
    def send_notification_signal(self):
        friend_request_sent.send(sender=self.__class__, from_account=self.from_account, to_account=self.to_account)

    def accept(self):
        self.status = self.ACCEPTED
        self.save(update_fields=['status'])
        friend_request_accepted.send(sender=self.__class__, from_account=self.from_account, to_account=self.to_account)

    def reject(self):
        self.status = self.REJECTED
        self.save(update_fields=['status'])
        friend_request_rejected.send(sender=self.__class__, from_account=self.from_account, to_account=self.to_account)
