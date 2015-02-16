from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class ActivityManager(models.Manager):

    def __create_activity(self, type, profile, content, to_activity, to_publication, to_profile):
        if not profile:
            raise ValueError('No profile given!')
        if to_activity and to_publication and to_profile:
            raise ValueError('Can\'t create an activity regarding more than one instance!')
        elif not to_activity and not to_publication and not to_profile:
            raise ValueError('Can\'t create an activity based regarding nothing!')
        return Activity.objects.create(type=type, profile=profile, to_activity=to_activity, to_publication=to_publication, to_profile=to_profile)

    def comment(self, profile, content, to_activity, to_publication):
        if not content:
            raise ValueError('Can\'t add an empty comment!')
        return self.__create_activity(Activity.COMMENT, profile, content, to_activity, to_publication, None)

    def like(self, profile, to_activity, to_publication):
        return self.__create_activity(Activity.LIKE, profile, '', to_activity, to_publication, None)

    def profile_post(self, profile, content, to_profile):
        if not content:
            raise ValueError('Can\'t add an empty profile post!')
        return self.__create_activity(Activity.PROFILE_POST, profile, content, None, None, to_profile)


class Activity(models.Model):
    LIKE, COMMENT, BEFRIEND, PUBLISH, PROFILE_POST, DELETE = range(6)
    TYPE_CHOICES = (
        (LIKE, 'Like'),
        (COMMENT, 'Comment'),
        (BEFRIEND, 'Befriend'),
        (PUBLISH, 'Publish'),
        (PROFILE_POST, 'Profile Post'),
        (DELETE, 'Delete'),
    )
    type = models.SmallIntegerField(choices=TYPE_CHOICES, default=LIKE)
    profile = models.ForeignKey('profiles.Profile')
    date = models.DateTimeField(auto_now_add=True)
    objects = ActivityManager()

    # related to comment or to_profile post
    last_modified = models.DateTimeField(auto_now=True, null=True)
    content = models.TextField(max_length=500, blank=True, default='')
    # to one of them
    to_activity = models.ForeignKey('self', null=True)
    to_publication = models.ForeignKey('feeds.Publication', null=True)
    to_profile = models.ForeignKey('profiles.Profile', null=True)

    def edit(self, new_content):
        if self.type != self.COMMENT:
            raise ValueError('Can\'t edit a non-comment!')
        if not new_content:
            return self
        self.content = new_content
        return self.save()
