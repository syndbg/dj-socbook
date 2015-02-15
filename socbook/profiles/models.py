from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    account = models.ForeignKey('accounts.Account')
    location = models.CharField(max_length=75, blank=True)
    friends = models.ManyToManyField('self', null=True, blank=True)

    @receiver(post_save, sender='accounts.Account')
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(account=instance)
