from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.signals import account_befriended, friend_request_accepted, friend_request_rejected, friend_request_sent, new_profile_created


class AccountManager(BaseUserManager):

    def __create_user(self, email, password, is_staff, is_superuser,
                      first_name, last_name):
        if not email:
            raise ValueError('Accounts must have an email address')

        email = self.normalize_email(email)
        user = self.model(username=email, email=email,
                          is_staff=is_staff, is_superuser=is_superuser,
                          first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, first_name='', last_name=''):
        return self.__create_user(email, password, False, False,
                                  first_name, last_name)

    def create_superuser(self, email, password, first_name='', last_name=''):
        return self.__create_user(email, password, True, True,
                                  first_name, last_name)


class Account(AbstractUser):
    MALE, FEMALE, SECRET = range(3)
    GENDERS = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (SECRET, 'Secret'))

    gender = models.SmallIntegerField(choices=GENDERS, default=SECRET)
    birthday = models.DateField(null=True)
    friends = models.ManyToManyField('self', symmetrical=True)
    location = models.CharField(max_length=75, blank=True)
    site = models.URLField(blank=True)

    AbstractUser._meta.get_field('first_name').help_text = 'Your first name'
    AbstractUser._meta.get_field('last_name').help_text = 'Your last name'
    AbstractUser._meta.get_field('email').help_text = 'The email you will use to login and restore your password if forgotten.'
    AbstractUser._meta.get_field('email')._unique = True
    AbstractUser._meta.get_field('username').max_length = 75
    objects = AccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def befriend(self, other_account):
        """Adds accounts in both accounts' friends fields and emits a signal for Activity and Notification to pick up."""
        if not self.is_friend(other_account):
            self.friends.add(other_account)
            self.save()
            other_account.friends.add(self)
            other_account.save()
            account_befriended.send(sender=self.__class__, account=self, other_account=other_account)

    def unfriend(self, other_account):
        if self.is_friend(other_account):
            self.friends.remove(other_account)
            self.save()
            other_account.friends.remove(self)
            other_account.save()

    def is_friend(self, other_account):
        return self in other_account.friends.all() and other_account in self.friends.all()

    def send_friend_request(self, to_account):
        try:
            return FriendRequest.objects.create(from_account=self, to_account=to_account)
        except Exception:
            raise ValueError('Friend request already sent')


class Profile(models.Model):
    account = models.OneToOneField(Account, related_name='profile')
    display_name = models.CharField(max_length=100, blank=True, help_text='The <display_name> that will be used in the URL to reach this profile.')

    def get_absolute_url(self):
        profile_name = self.display_name or self.account.username
        return reverse('accounts:profile', args=[profile_name])

    @receiver(post_save, sender=Account)
    def create_profile(sender, instance, created, **kwargs):
        """Creates a Profile and emits a signal for Activity to pick up and create an Activity and later Notification."""
        if created:
            Profile.objects.create(account=instance)
            new_profile_created.send(sender=instance.__class__, account=instance)


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
        """Accepts a FriendRequest, emits a friend_request_accepted signal for Notification to pick up,
           befriends from_account and to_account and emits an account_befriended signal for Activity to pick up."""
        self.status = self.ACCEPTED
        self.save(update_fields=['status'])
        friend_request_accepted.send(sender=self.__class__, from_account=self.from_account, to_account=self.to_account)
        self.from_account.befriend(self.to_account)

    def reject(self):
        """Rejects a FriendRequest and emits a friend_request_rejected signal for Notification to pick up"""
        self.status = self.REJECTED
        self.save(update_fields=['status'])
        friend_request_rejected.send(sender=self.__class__, from_account=self.from_account, to_account=self.to_account)
