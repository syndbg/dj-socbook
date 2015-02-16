from django.db import models


class ActivityManager(models.Manager):

    def __create_activity(self, type, profile, content, activity, publication):
        if not profile:
            raise ValueError('No profile given!')
        if activity and publication:
            raise ValueError('Can\'t like/comment on both activity and publication at the same time!')
        elif not activity and not publication:
            raise ValueError('Can\'t like/comment nothingness!')

        return Activity.objects.create(type=type, profile=profile, content=content, activity=activity, publication=publication)

    def comment(self, profile, content, activity, publication):
        if not content:
            raise ValueError('Can\'t add an empty comment!')
        return self.__create_activity(Activity.COMMENT, profile, content, activity, publication)

    def like(self, profile, activity, publication):
        return self.__create_activity(Activity.LIKE, profile, '', activity, publication)


class Activity(models.Model):
    LIKE, COMMENT = range(2)
    TYPE_CHOICES = (
        (LIKE, 'Like'),
        (COMMENT, 'Comment'))
    type = models.SmallIntegerField(choices=TYPE_CHOICES, default=LIKE)
    profile = models.ForeignKey('profiles.Profile')
    date = models.DateTimeField(auto_now_add=True)

    # comment-related
    last_modified = models.DateTimeField(auto_now=True, null=True)
    content = models.TextField(max_length=500, blank=True, default='')
    # regarding one of both
    other_activity = models.ForeignKey('self', null=True)
    publication = models.ForeignKey('feeds.Publication', null=True)

    objects = ActivityManager()

    def edit(self, new_content):
        if self.type != self.COMMENT:
            raise ValueError('Can\'t edit a non-comment!')
        if not new_content:
            return self
        self.content = new_content
        return self.save()
