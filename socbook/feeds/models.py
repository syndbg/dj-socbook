from django.db import models

from activities.models import Activity


class Publication(models.Model):
    PUBLIC, PRIVATE = range(2)
    VISIBILITY_CHOICES = (
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private'))

    author = models.ForeignKey('profiles.Profile', null=True)
    title = models.CharField(max_length=125, blank=False)
    content = models.TextField(max_length=500, blank=False)
    visibility = models.SmallIntegerField(choices=VISIBILITY_CHOICES, default=PUBLIC)

    @property
    def likes(self):
        return Activity.objects.filter(type=Activity.LIKE, publication=self)

    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def comments(self):
        return Activity.objects.filter(type=Activity.COMMENT, publication=self)

    @property
    def comments_count(self):
        return self.comments.count()
