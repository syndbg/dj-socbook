from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class ActivityManager(models.Manager):

    def __create_activity(self, type, profile, content, to_activity, to_publication, to_profile):
        if not profile:
            raise ValueError('No profile given!')
        if to_activity and to_publication and to_profile:
            raise ValueError(
                'Can\'t create an activity regarding more than one instance!')
        elif not to_activity and not to_publication and not to_profile:
            raise ValueError(
                'Can\'t create an activity based regarding nothing!')
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
        (LIKE, 'like'),
        (COMMENT, 'comment'),
        (BEFRIEND, 'befriendment'),
        (PUBLISH, 'publication'),
        (PROFILE_POST, 'profile post'),
        (DELETE, 'deletetion'),
    )
    type = models.SmallIntegerField(choices=TYPE_CHOICES, default=LIKE)
    profile = models.ForeignKey('profiles.Profile', related_name='activities')
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

    @receiver(post_save, sender='activities.Activity')
    def create_notifications(sender, instance, created, raw, using, update_fields, **kwargs):
        pass


class Notification(models.Model):
    activity = models.ForeignKey(Activity)
    date = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
    type = models.SmallIntegerField(
        choices=Activity.TYPE_CHOICES, default=Activity.LIKE)

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
