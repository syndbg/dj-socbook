from django.db import models

from activities.models import Activity


class Publication(models.Model):
    PUBLIC, FRIENDS, PRIVATE = range(3)
    VISIBILITY_CHOICES = (
        (PUBLIC, 'Public'),
        (FRIENDS, 'Friends'),
        (PRIVATE, 'Private'))

    author = models.ForeignKey('profiles.Profile', null=True)
    title = models.CharField(max_length=125, blank=False)
    content = models.TextField(max_length=500, blank=False)
    visibility = models.SmallIntegerField(choices=VISIBILITY_CHOICES, default=PUBLIC)

    @property
    def likes(self):
        return Activity.objects.filter(type=Activity.LIKE, publication=self)

    @property
    def first_like_and_others(self):
        likes = self.likes.all()
        return likes[0], likes[1:]

    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def comments(self):
        return Activity.objects.filter(type=Activity.COMMENT, publication=self)

    @property
    def comments_count(self):
        return self.comments.count()
